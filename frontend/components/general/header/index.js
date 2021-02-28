import Head from 'next/head';
import Link from 'next/link';
import React from 'react';
import { HeaderContainer, Logo, MenuLink } from './styled';
import { BiMessageAltDots } from 'react-icons/bi';
import { Flex } from '../flex/styled';

import { observer } from 'mobx-react';
import MessagesStore from '../../../mobx/messagesStore';

const Header = observer(({ pathname }) => {
  const { count, authorized } = MessagesStore;

  return (
    <HeaderContainer>
      <div style={{ height: '44px', paddingRight: '50px' }}>
        <Link href='/' passHref>
          <Logo>
            SlowMAIL <BiMessageAltDots />
          </Logo>
        </Link>
      </div>
      <Flex height={'44px'} padding={'0 0 6px'} width={'450px'} alignItemsEnd>
        {authorized
          ? [
              { name: 'Главная', link: '/' },
              { name: `Сообщения (${count})`, link: '/messages' },
              { name: 'Найти друзяшек', link: '/findFriends' },
              { name: 'Выйти', link: '/logout' },
            ].map(({ name, link }, i) => (
              <Link href={link} passHref key={i}>
                <MenuLink {...(pathname === link ? { active: true } : {})}>{name}</MenuLink>
              </Link>
            ))
          : ''}
      </Flex>
    </HeaderContainer>
  );
});

export default Header;
