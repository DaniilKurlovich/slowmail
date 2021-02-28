import Head from 'next/head';
import { useEffect } from 'react';
import {
  acceptHandshake,
  getCategories,
  getListHandshake,
  getMyCategories,
  getPossibleFriends,
  sendHandshake,
} from '../api/users';
import { useCookies } from 'react-cookie';
import { useState } from 'react';
import { setMyCategories } from './../api/users';
import { RecommendedFriend } from '../components/pages/findFriends/styled';
import { Flex } from '../components/general/flex/styled';
import { Button } from '../components/pages/index/styled';

export default function FindFriends() {
  const [cookies] = useCookies(['token']);
  const [inHandshakes, setInHandshakes] = useState([]);
  const [possibleFriends, setPossibleFriends] = useState([]);

  const load = async () => {
    const { data: handshakes } = await getListHandshake({ token: cookies.token });
    const { data: loadedPossibleFriends } = await getPossibleFriends({ token: cookies.token });

    setInHandshakes(handshakes.in);
    setPossibleFriends(loadedPossibleFriends);
  };

  const sendRequest = async (userId) => {
    sendHandshake({ token: cookies.token, toUserId: userId });
  };

  const acceptRequest = async (userId) => {
    await acceptHandshake({ token: cookies.token, userId });

    setInHandshakes(inHandshakes.filter((friend) => friend.id !== userId));
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div>
      <Head>
        <title>Поиск друзей - SlowMAIL</title>
        <link rel='icon' href='/favicon.ico' />
      </Head>
      <main>
        <h1>Поиск друзей</h1>
        <h3>Заявки:</h3>
        <div>
          {inHandshakes.length === 0 && <>Заявок нет</>}
          {inHandshakes.map((handshakeFriend) => (
            <RecommendedFriend key={handshakeFriend.id}>
              <div>
                <b>ID:</b> {handshakeFriend.id}
              </div>
              <div>
                <b>Полное имя:</b> {handshakeFriend.full_name}
              </div>
              <div>
                <b>Интересы:</b> {handshakeFriend.category.join(', ')}
              </div>
              <Flex margin={'20px 0 0 0'}>
                <Button onClick={() => acceptRequest(handshakeFriend.id)}>Принять заявку</Button>
              </Flex>
            </RecommendedFriend>
          ))}
        </div>
        <h3>Рекомендации:</h3>
        <div>
          {possibleFriends.length === 0 && <>Не удалось найти подходящих людей</>}
          {possibleFriends.map((friend) => (
            <RecommendedFriend key={friend.id}>
              <div>
                <b>ID:</b> {friend.id}
              </div>
              <div>
                <b>Полное имя:</b> {friend.full_name}
              </div>
              <div>
                <b>Интересы:</b> {friend.category.join(', ')}
              </div>
              <Flex margin={'20px 0 0 0'}>
                <Button
                  onClick={() => {
                    sendRequest(friend.id);
                  }}
                >
                  Отправить заявку
                </Button>
              </Flex>
            </RecommendedFriend>
          ))}
        </div>
      </main>
    </div>
  );
}
