import axios from 'axios';
import { URL } from './config';

export const getMessages = ({ token, to_addr }) =>
  axios.get(`${URL}/getMessages`, {
    params: { to_addr },
    headers: { authorization: token },
  });

export const sendMessage = ({ token, to_addr, content, delay }) =>
  axios.post(`${URL}/sendMessage`, undefined, {
    params: { to_addr, content, delay },
    headers: { authorization: token },
  });

export const markAsRead = ({ token, id_letter }) =>
  axios.post(`${URL}/markAsRead`, {
    params: { id_letter },
    headers: { authorization: token },
  });
