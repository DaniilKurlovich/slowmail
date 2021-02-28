import Head from 'next/head';
import Router from 'next/router';
import { useState } from 'react';
import { useCookies } from 'react-cookie';
import { observer } from 'mobx-react';
import { authorize, signup } from './../api/auth';
import MessagesStore from '../mobx/messagesStore';
import {
  Button,
  Input,
  MainContainer,
  SwitchButton,
  SwitchContainer,
  Tag,
} from './../components/pages/index/styled';
import { Flex } from '../components/general/flex/styled';
import { useEffect } from 'react';
import { getCategories, getMyCategories, setMyCategories } from '../api/users';

function Home() {
  const [loginUsername, setLoginUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');

  const [registerUsername, setRegisterUsername] = useState('');
  const [registerPassword, setRegisterPassword] = useState('');
  const [registerFirstName, setRegisterFirstName] = useState('');
  const [registerLastName, setRegisterLastName] = useState('');

  const [error, setError] = useState('');
  const [cookies, setCookie] = useCookies(['token']);

  const [page, setPage] = useState('auth');

  const { authorized } = MessagesStore;

  async function handleAuthorize(e) {
    e.preventDefault();

    if (!loginUsername || !loginPassword) {
      setError('Вы не заполнили логин или пароль.');
      return;
    }

    setError('');

    const formData = new FormData();
    formData.append('username', loginUsername);
    formData.append('password', loginPassword);

    try {
      const result = await authorize(formData);

      setCookie('token', result?.data?.access_token, { path: '/' });

      Router.reload();
    } catch (err) {
      setError('Введен неверный логин или пароль');
    }
  }

  async function handleRegister(e) {
    e.preventDefault();

    if (!registerUsername || !registerPassword || !registerFirstName || !registerLastName) {
      setError('Вы не заполнили некоторые поля.');
      return;
    }

    setError('');

    const formData = new FormData();
    formData.append('username', registerUsername);
    formData.append('password', registerPassword);
    formData.append('first_name', registerFirstName);
    formData.append('last_name', registerLastName);

    try {
      const result = await signup(formData);

      setCookie('token', result?.data?.access_token, { path: '/' });

      Router.reload();
    } catch (err) {
      setError('Данный аккаунт уже существует');
    }
  }

  const [allCategories, setAllCategories] = useState([]);

  const load = async () => {
    const { data: categories } = await getCategories({ token: cookies.token });
    const { data: myCategories } = await getMyCategories({ token: cookies.token });

    const myCategoriesSet = new Set(myCategories.categories);

    setAllCategories(
      categories.map((categoryName) => ({
        active: myCategoriesSet.has(categoryName),
        name: categoryName,
      }))
    );
  };

  const toggleActive = async (index) => {
    if (!allCategories[index]) {
      return;
    }

    const newCategories = allCategories.map((e, i) => ({
      ...e,
      active: i === index ? !e.active : e.active,
    }));

    setAllCategories(newCategories);

    setMyCategories({
      token: cookies.token,
      listCategories: newCategories
        .filter((category) => category.active)
        .map((category) => category.name),
    });
  };

  useEffect(() => {
    if (authorized) {
      load();
    }
  }, [authorized]);

  return (
    <div>
      <Head>
        <title>Главная - SlowMAIL</title>
        <link rel='icon' href='/favicon.ico' />
      </Head>

      <MainContainer>
        <h1>Главная</h1>
        {authorized ? (
          <>
            <div>Выберите категории общения которые вам интересны:</div>
            <Flex flexFlowWrap={true} width={'400px'}>
              {[
                allCategories.map((category, i) => (
                  <Tag active={category.active} onClick={() => toggleActive(i)} key={i}>
                    {category.name}
                  </Tag>
                )),
              ]}
            </Flex>
            <div>Исходя из них мы будем рекомендовать вам друзей</div>
          </>
        ) : (
          <>
            <SwitchContainer>
              <SwitchButton
                active={page === 'auth' ? page : undefined}
                onClick={() => {
                  setError('');
                  setPage('auth');
                }}
              >
                Авторизация
              </SwitchButton>
              <SwitchButton
                active={page === 'registration' ? page : undefined}
                onClick={() => {
                  setError('');
                  setPage('registration');
                }}
              >
                Регистрация
              </SwitchButton>
            </SwitchContainer>

            {page === 'auth' ? (
              <form onSubmit={handleAuthorize}>
                <Input
                  type='text'
                  value={loginUsername}
                  onChange={(e) => setLoginUsername(e.target.value)}
                  placeholder='Введите логин'
                />
                <br />
                <Input
                  type='password'
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  placeholder='Введите пароль'
                />{' '}
                <br />
                {error && <div style={{ color: 'red' }}>{error}</div>}
                <br />
                <Button>Отправить</Button>
              </form>
            ) : (
              <form onSubmit={handleRegister}>
                <Input
                  type='text'
                  value={registerUsername}
                  onChange={(e) => setRegisterUsername(e.target.value)}
                  placeholder='Введите логин'
                />
                <br />
                <Input
                  type='password'
                  value={registerPassword}
                  onChange={(e) => setRegisterPassword(e.target.value)}
                  placeholder='Введите пароль'
                />
                <br />
                <Input
                  type='text'
                  value={registerFirstName}
                  onChange={(e) => setRegisterFirstName(e.target.value)}
                  placeholder='Введите имя'
                />
                <br />
                <Input
                  type='text'
                  value={registerLastName}
                  onChange={(e) => setRegisterLastName(e.target.value)}
                  placeholder='Введите фамилия'
                />
                <br />
                {error && <div style={{ color: 'red' }}>{error}</div>}
                <br />
                <Button>Отправить</Button>
              </form>
            )}
          </>
        )}
      </MainContainer>
    </div>
  );
}

export default observer(Home);
