import axios, { AxiosHeaders, InternalAxiosRequestConfig } from 'axios';
import { isTokenExpired } from './tokenExpired';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8081/user',
});

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {

    if (config.url?.includes('/login') || config.url?.includes('/signup')) {
      return config;
    }

    const token = localStorage.getItem('usertoken');

    if (isTokenExpired(token)) {
      localStorage.removeItem('usertoken');
      window.location.href = '/';
      throw new axios.Cancel('Token expired');
    }

    config.headers = new AxiosHeaders(config.headers);
    if (token) {
      config.headers.set('Authorization', `Bearer ${token}`);
    }

    return config;
  },
  error => Promise.reject(error)
);

export default api;
