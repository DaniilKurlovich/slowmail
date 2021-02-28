import { action, observable, makeObservable, computed } from 'mobx';

class Messages {
  constructor() {
    makeObservable(this);
  }

  @observable myId = -1;
  @observable authorized = undefined;
  @observable messages = [];
  @observable chats = [];

  @computed get count() {
    let sum = 0;

    for (let i = 0; i < this.chats.length; i++) {
      const chat = this.chats[i];

      for (let j = chat.messages.length - 1; j >= 0; j--) {
        const message = chat.messages[j];

        if (!message.readed && !message.my) {
          sum++;
        }
      }
    }

    return sum;
  }

  @action setMyId = (myId) => {
    this.myId = myId;
  };

  @action setAuthorized = (authorized) => {
    this.authorized = authorized;
  };

  @action save = (messages) => {
    this.messages = messages;
  };

  @action markReaded = (chatIndex, messageIndex) => {
    this.chats[chatIndex].messages[messageIndex].readed = true;
  };

  @action addMessage = (chatIndex, message) => {
    this.chats[chatIndex].messages.unshift(message);
  };

  @action setChats = (chats) => {
    this.chats = chats;
  };

  @action clear = () => {
    this.messages = [];
  };
}

const MessagesStore = new Messages();
export default MessagesStore;
