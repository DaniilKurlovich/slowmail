import Head from 'next/head';
import { observer } from 'mobx-react';
import MessagesStore from './../mobx/messagesStore';
import { useEffect } from 'react';
import { toJS } from 'mobx';
import Dialogs from '../components/pages/messages/dialogs/index';
import { Main } from '../components/general/main/styled';

const Messages = function () {
    const { messages, count, add } = MessagesStore;

    // useEffect(() => {
    //     const interval = setInterval(() => {
    //         increase();
    //     }, 1000);

    //     return () => {
    //         clearInterval(interval);
    //     };
    // }, []);

    return (
        <>
            <Head>
                <title>Сообщения ({count}) - SlowMAIL</title>
                <link rel='icon' href='/favicon.ico' />
            </Head>
            <Main>
                <Dialogs />
            </Main>
        </>
    );
};

export default observer(Messages);
