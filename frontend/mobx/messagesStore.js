import { action, observable, makeObservable, computed } from 'mobx';

class Messages {
  constructor() {
    makeObservable(this);
  }

  @observable myId = -1;
  @observable authorized = undefined;
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

  @action markReaded = (chatIndex, messageIndex) => {
    this.chats[chatIndex].messages[messageIndex].readed = true;
  };

  @action addChat = (friend) => {
    this.chats.push({
      friend,
      messages: [],
    });
  };

  @action markReadedById = (id) => {
    for (let i = 0; i < this.chats.length; i++) {
      for (let j = 0; j < this.chats[i].messages.length; j++) {
        if (this.chats[i].messages[j].id === id) {
          this.chats[i].messages[j].readed = true;

          break;
        }
      }
    }
  };

  @action addMessage = (chatIndex, message) => {
    this.chats[chatIndex].messages.unshift(message);
  };

  @action addMessageByFriendId = (friendId, message) => {
    for (let i = 0; i < this.chats.length; i++) {
      if (this.chats[i].friend.id === friendId) {
        this.chats[chatIndex].messages.unshift(message);

        break;
      }
    }
  };

  @action setChats = (chats) => {
    this.chats = chats;
  };
}

const MessagesStore = new Messages();
export default MessagesStore;
