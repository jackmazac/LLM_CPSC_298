import express from 'express';
import { register, login } from './services/authService';
import { LoginCredentials } from './interfaces/LoginCredentials';

const app = express();
app.use(express.json());

app.post('/register', async (req, res) => {
  const { username, password, email } = req.body;

  try {
    const user = await register(username, password, email);
    res.status(201).json(user);
  } catch (error) {
    console.error('Registration failed:', error);
    res.status(400).json({ error: 'Registration failed' });
  }
});

app.post('/login', async (req, res) => {
  const credentials: LoginCredentials = req.body;

  try {
    const user = await login(credentials);
    if (user) {
      res.json(user);
    } else {
      res.status(401).json({ error: 'Invalid credentials' });
    }
  } catch (error) {
    console.error('Login failed:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
