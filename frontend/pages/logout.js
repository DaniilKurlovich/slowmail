import { observer } from 'mobx-react';
import { useEffect } from 'react';
import { useCookies } from 'react-cookie';

const Logout = function () {
  const [cookies, setCookie] = useCookies(['token']);

  useEffect(() => {
    setCookie('token', '');

    window.location.href = '/';
  });

  return <></>;
};

export default observer(Logout);
