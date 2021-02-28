import axios from 'axios';
import { URL } from './config';

export const authorize = (formData) => axios.post(`${URL}/token`, formData);
export const signup = (formData) => axios.post(`${URL}/signup`, formData);
