import styled from 'styled-components';

export const DialogsContainer = styled.div`
    display: grid;
    grid-template-columns: 300px auto;
    grid-template-rows: auto 100px;
    grid-template-areas: 'dialogsList messages' 'dialogsList newMessage';
    width: 100%;
    height: calc(100vh - 100px - 70px - 50px);
    box-sizing: border-box;
    background: #e8f9dc;
    overflow: hidden;
    border-radius: 10px;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.2);
`;

export const DialogsList = styled.div`
    padding: 10px;
    box-sizing: border-box;
    background: #052639;
    color: #fbfef9;
    grid-area: dialogsList;

    overflow-y: auto;
    height: 100%;

    &::-webkit-scrollbar {
        width: 5px;
    }

    &::-webkit-scrollbar-track {
        box-shadow: inset 0 0 4px rgba(0, 0, 0, 0.3);
    }

    &::-webkit-scrollbar-thumb {
        background-color: #7e1946;
    }
`;

export const DialogMessages = styled.div`
    padding: 20px 10px;
    box-sizing: border-box;
    background: #fbfef9;
    color: #000004;
    display: flex;
    flex-direction: column-reverse;
    align-items: flex-start;
    grid-area: messages;

    overflow-y: auto;
    height: 100%;

    &::-webkit-scrollbar {
        width: 5px;
    }

    &::-webkit-scrollbar-track {
        box-shadow: inset 0 0 4px rgba(0, 0, 0, 0.3);
    }

    &::-webkit-scrollbar-thumb {
        background-color: #052639;
    }
`;

export const Message = styled.div`
    display: inline-block;
    background: ${(props) => (props.unreaded ? '#ccc' : props.my ? '#FCEEF4' : '#ECF7FD')};
    ${(props) => (props.my ? 'align-self: flex-end;' : '')}
    padding: 18px 20px;
    line-height: 26px;
    font-size: 16px;
    word-break: break-all;
    max-width: 500px;
    position: relative;
    transition: 1s background;
    ${(props) => (props.my ? 'margin-right: 40px;' : 'margin-left: 40px;')}

    ${(props) => (props.my ? 'border-bottom-left-radius' : 'border-bottom-right-radius')}: 15px;
    ${(props) => (props.my ? 'border-top-left-radius' : 'border-top-right-radius')}: 15px;
    ${(props) => (props.my ? 'border-bottom-right-radius' : 'border-bottom-left-radius')}: 15px;

    &:after {
        border: solid transparent;
        content: '';
        height: 0;
        width: 0;
        position: absolute;
        pointer-events: none;
        ${(props) => (props.my ? 'border-left-color: #FCEEF4;' : 'border-right-color: #ECF7FD;')}

        top: 0;
        ${(props) => (props.my ? 'right' : 'left')}: -10px;
        margin-${(props) => (props.my ? 'right' : 'left')}: -10px;
        border-width: 10px;
    }

    &:not(:last-child) {
        margin-top: 15px;
    }
`;

export const ChatAvatar = styled.div`
    position: absolute;
    ${(props) => (props.my ? 'right' : 'left')}: -43px;
    padding: 0;
    overflow: hidden;
    border-radius: 20px;
    top: -5px;
    width: 30px;
    height: 30px;

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
    }
`;

export const Friend = styled.div`
    display: flex;
    padding: 10px 20px;
    cursor: pointer;
    background: ${(props) => (props.current ? '#2F0F13' : 'none')};
    border-radius: 5px;

    &:hover {
        background: ${(props) => (props.current ? '#2F0F13' : '#0A3F5C')};
    }
`;

export const FriendAvatar = styled.div`
    overflow: hidden;
    border-radius: 50%;
    width: 60px;
    height: 60px;

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
    }
`;

export const FriendStatus = styled.div`
    color: #ebc1c9;
    font-size: 13px;
    line-height: 17px;
`;

export const DialogNewMessage = styled.div`
    background: ${(props) => (props.chatOpened ? '#ccc' : '#fbfef9')};
    display: flex;
    align-items: center;
    justify-content: space-around;
    grid-area: newMessage;

    textarea {
        padding: 8px;
        resize: none;
        width: 70%;
        font-size: 14px;
        outline: none;
        border-radius: 5px;
        border: 1px dashed transparent;
    }

    textarea:focus,
    textarea:hover {
        border: 1px solid #2f0f13;
    }

    button {
        cursor: pointer;
        border-radius: 20px;
        padding: 10px 15px;
        color: #ffffff;
        background: #a63446;
        border: none;
        outline: none;
    }
`;
