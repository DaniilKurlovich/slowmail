import { Layout } from '../components/general/layout/styled';
import '../styles/globals.css';
import Footer from '../components/general/footer';
import Header from '../components/general/header';
import { useEffect } from 'react';
import { myFriends, getMyInfo } from '../api/users';
import { useCookies } from 'react-cookie';

import MessagesStore from '../mobx/messagesStore';
import { observer } from 'mobx-react';
import { getMessages, sendMessage } from '../api/messages';
import messages from './messages';
import { useRouter } from 'next/router';
import axios from 'axios';

function MyApp({ Component, pageProps, pathname }) {
  const [cookies, setCookie] = useCookies(['token']);
  const {
    setMyId,
    myId,
    setChats,
    authorized,
    setAuthorized,
    addMessage,
    markReadedById,
    addChat,
  } = MessagesStore;
  const router = useRouter();

  useEffect(() => {
    if (authorized === false && pathname !== '/') {
      router.push('/');
    }
  }, [pathname, authorized]);

  async function load() {
    let localAuthorized = false;
    let localId = undefined;

    try {
      const { data: info } = await getMyInfo(cookies.token);
      setMyId(info.id);
      localId = info.id;

      setAuthorized(true);
      localAuthorized = true;
    } catch (err) {
      setAuthorized(false);
      if (err?.response?.status === 401) {
        console.log('Тут эта нада заканчивать');

        const { pathname } = router;
        if (pathname !== '/') {
          Router.push('/');
        }
      }
    }

    if (!localAuthorized) {
      return;
    }

    let {
      data: { friends },
    } = await myFriends({ token: cookies.token });

    // console.log(friends);

    const chats = await Promise.all(
      friends.map(async (item, index) => {
        const { data: messagesWithFriend } = await getMessages({
          token: cookies.token,
          to_addr: item.id,
        });

        return {
          friend: item,
          messages: messagesWithFriend.map((message) => ({
            ...message,
            text: message.letter,
            readed: message.mark_as_read,
            my: message.is_your_message,
          })),
        };
      })
    );

    setChats(chats);

    let socket = new WebSocket('ws://localhost:8888/notification');

    socket.onopen = function (e) {
      socket.send(JSON.stringify({ from_id: localId }));
    };

    socket.onmessage = function (e) {
      const data = JSON.parse(e.data);

      if (data.type === 'message') {
        const info = JSON.parse(data.data);
        const { from_id } = info;

        for (let i = 0; i < chats.length; i++) {
          if (chats[i].friend.id === from_id) {
            addMessage(i, {
              ...info,
              text: info.letter,
              readed: info.mark_as_read,
              my: info.is_your_message,
            });

            break;
          }
        }
      } else if (data.type === 'mark_read') {
        const { id } = data.data;

        markReadedById(id);
      } else if (data.type === 'new_friend') {
        const friend = JSON.parse(data.data);

        addChat(friend);
      }
    };
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <Layout>
      <Header pathname={pathname} />
      <Component {...pageProps} />
      <Footer />
    </Layout>
  );
}

MyApp.getInitialProps = async ({ Component, ctx }) => {
  const { pathname } = ctx;

  let pageProps = {};
  if (Component.getInitialProps) {
    pageProps = await Component.getInitialProps(ctx);
  }

  return { pageProps, pathname };
};

export default observer(MyApp);
