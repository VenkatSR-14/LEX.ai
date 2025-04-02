import './Modal.scss';
import { useDispatch } from 'react-redux';
import { AppDispatch } from '../../store';
import { update } from '../../Slices/loginSlice';
import { FormEvent, useState } from 'react';
import api from '../../middleware/api';

function Modal() {
  const dispatch = useDispatch<AppDispatch>();
  const [userName, setUsername] = useState('');
  const [firstName, setFirstname] = useState('');
  const [lastName, setLastname] = useState('');
  const [password, setPassword] = useState('');
  const [isSignup, setIsSignup] = useState(false);
  const [email, setEmail] = useState('');
  const [role, setRole] = useState<'User' | 'Admin'>('User');

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const payload = isSignup
        ? { userName, firstName, lastName, email, password, role }
        : { userName, password };

      const endpoint = isSignup ? 'signup' : 'login';
      const response = await api.post(`/${endpoint}`, payload);
      localStorage.setItem('usertoken', response.data.token);

      window.location.href = '/';
    } catch (error) {
      console.error(`${isSignup ? 'Signup' : 'Login'} failed:`, error);
    }
  };

  return (
    <div
      className="modal-outer d-flex justify-content-center align-items-center"
      onClick={() => dispatch(update())}
    >
      <div className="modal-inner" onClick={(e) => e.stopPropagation()}>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="username" className="form-label">Username</label>
            <input type="text" id="username" className="form-control" onChange={(e) => setUsername(e.target.value)} required />
          </div>

          {isSignup && (
            <>
              <div className="mb-3">
                <label htmlFor="firstName" className="form-label">First Name</label>
                <input type="text" id="firstName" className="form-control" onChange={(e) => setFirstname(e.target.value)} required />
              </div>
              <div className="mb-3">
                <label htmlFor="lastName" className="form-label">Last Name</label>
                <input type="text" id="lastName" className="form-control" onChange={(e) => setLastname(e.target.value)} required />
              </div>
              <div className="mb-3">
                <label htmlFor="email" className="form-label">Email</label>
                <input type="email" id="email" className="form-control" onChange={(e) => setEmail(e.target.value)} required />
              </div>
              <div className="mb-3">
                <label htmlFor="role" className="form-label">Role</label>
                <select className="form-select" value={role} onChange={(e) => setRole(e.target.value as 'User' | 'Admin')}>
                  <option value="User">User</option>
                  <option value="Admin">Admin</option>
                </select>
              </div>
            </>
          )}

          <div className="mb-3">
            <label htmlFor="password" className="form-label">Password</label>
            <input type="password" id="password" className="form-control" onChange={(e) => setPassword(e.target.value)} required />
          </div>

          <div className="d-flex justify-content-center">
            <button type="submit" className="btn btn-primary">
              {isSignup ? 'Sign Up' : 'Login'}
            </button>
          </div>

          <p className="text-center mt-2">
            {isSignup ? "Already have an account?" : "Don't have an account?"}{' '}
            <span style={{ cursor: 'pointer', color: 'blue' }} onClick={() => setIsSignup(!isSignup)}>
              {isSignup ? "LOGIN" : "SIGNUP"}
            </span>
          </p>
        </form>
      </div>
    </div>
  );
}

export default Modal;
