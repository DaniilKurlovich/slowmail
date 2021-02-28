import React, { createRef, useEffect, useState } from 'react';
import { Flex } from '../../../general/flex/styled';
import {
  DialogsContainer,
  DialogsList,
  DialogMessages,
  Message,
  ChatAvatar,
  Friend,
  FriendAvatar,
  FriendStatus,
  DialogNewMessage,
} from './styled';
import MessagesStore from '../../../../mobx/messagesStore';
import { observer } from 'mobx-react';
import { sendMessage } from '../../../../api/messages';
import { useCookies } from 'react-cookie';
import { toJS } from 'mobx';
import { markAsRead } from './../../../../api/messages';

const Dialogs = () => {
  const chatRef = createRef();
  const { addMessage, markReaded, chats } = MessagesStore;

  const [cookies] = useCookies(['token']);
  const [currentChat, setCurrentChat] = useState(undefined);
  const [messageText, setMessageText] = useState('');

  useEffect(() => {
    chatRef.current.scrollTo({
      top: chatRef.current.scrollHeight - chatRef.current.clientHeight,
      left: 0,
    });
  }, [chatRef.current, currentChat]);

  useEffect(() => {
    if (currentChat === undefined) {
      return;
    }

    for (let i = 0; i < chats[currentChat].messages.length; i++) {
      const { readed, my } = chats[currentChat].messages[i];

      if (!readed && !my) {
        markReaded(currentChat, i);
        markAsRead({ token: cookies.token, id_letter: chats[currentChat].messages[i].id });
      }
    }
  }, [currentChat]);

  const sendMessageHandler = () => {
    if (currentChat === undefined || chats[currentChat]?.friend?.id === undefined) {
      return;
    }

    console.log(chats[currentChat]?.friend?.id);
    sendMessage({
      token: cookies.token,
      to_addr: chats[currentChat]?.friend?.id,
      content: messageText,
    });
    addMessage(currentChat, { my: true, readed: false, text: messageText });
  };

  return (
    <DialogsContainer>
      <DialogsList>
        {chats.map((chat, i) => (
          <Friend current={currentChat === i} onClick={() => setCurrentChat(i)} key={i}>
            <FriendAvatar>
              <img src='https://vk.com/images/camera_50.png?ava=1' />
            </FriendAvatar>
            <Flex padding={'0 10px'} column justifyContentCenter>
              <div>{chat.friend.full_name}</div>
              <FriendStatus>ID: {chat.friend.id}</FriendStatus>
            </Flex>
          </Friend>
        ))}
      </DialogsList>
      <DialogMessages ref={chatRef}>
        {currentChat !== undefined &&
          chats[currentChat].messages.map(({ text, my, readed }, i) => {
            return (
              <Message my={my} key={i} unreaded={!readed}>
                <ChatAvatar my={my}>
                  <img src='https://vk.com/images/camera_50.png?ava=1' />
                </ChatAvatar>
                {text}
              </Message>
            );
          })}
      </DialogMessages>
      <DialogNewMessage chatOpened={currentChat !== undefined}>
        {currentChat !== undefined && (
          <>
            <textarea
              placeholder={'Введите текст'}
              rows={'4'}
              value={messageText}
              onChange={(e) => {
                setMessageText(e.target.value);
              }}
            ></textarea>
            <button onClick={sendMessageHandler}>Отправить</button>
          </>
        )}
      </DialogNewMessage>
    </DialogsContainer>
  );
};

export default observer(Dialogs);
