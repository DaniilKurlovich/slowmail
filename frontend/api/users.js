import axios from 'axios';
import { URL } from './config';

export const getMyInfo = (token) =>
  axios.get(`${URL}/users/me`, { headers: { authorization: token } });

export const myFriends = ({ token, tags, limit }) =>
  axios.get(`${URL}/myFriends`, { params: { tags, limit }, headers: { authorization: token } });

export const getCategories = ({ token }) =>
  axios.get(`${URL}/categories`, { headers: { authorization: token } });

export const getMyCategories = ({ token }) =>
  axios.get(`${URL}/myCategories`, { headers: { authorization: token } });

export const setMyCategories = ({ token, listCategories }) =>
  axios.post(`${URL}/setCategories`, null, {
    params: {
      list_categories: listCategories.reduce((f, s) => `${f},${s}`),
    },
    headers: {
      authorization: token,
    },
  });

export const getPossibleFriends = ({ token }) =>
  axios.get(`${URL}/possibleFriends`, {
    headers: {
      authorization: token,
    },
  });

export const sendHandshake = ({ token, toUserId }) =>
  axios.post(`${URL}/sendHandshake`, null, {
    params: {
      to_user_id: toUserId,
    },
    headers: {
      authorization: token,
    },
  });

export const acceptHandshake = ({ token, userId }) =>
  axios.post(`${URL}/acceptHandshake`, null, {
    params: {
      user_id: userId,
    },
    headers: {
      authorization: token,
    },
  });

export const getListHandshake = ({ token }) =>
  axios.get(`${URL}/listHandshake`, {
    headers: {
      authorization: token,
    },
  });
