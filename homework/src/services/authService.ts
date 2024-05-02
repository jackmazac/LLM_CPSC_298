import { User, HashedPassword } from '../interfaces/User';
import { LoginCredentials } from '../interfaces/LoginCredentials';
import { hashPassword, comparePasswords } from '../utils/passwordUtils';
import { getUser, saveUser } from '../config/database';

async function register(username: string, password: string, email: string): Promise<User> {
  // Check if the username or email is already taken
  const existingUser = await getUser(username, email);
  if (existingUser) {
    throw new Error('Username or email already exists');
  }

  // Hash the password
  const hashedPassword: HashedPassword = await hashPassword(password);

  // Create a new user object
  const newUser: User = {
    id: generateUserId(),
    username,
    email,
    hashedPassword,
    createdAt: new Date(),
    updatedAt: new Date(),
  };

  // Save the user to the database
  await saveUser(newUser);

  return newUser;
}

async function login(credentials: LoginCredentials): Promise<User | null> {
  const { username, password } = credentials;

  // Retrieve the user from the database
  const user = await getUser(username);
  if (!user) {
    return null;
  }

  // Compare the provided password with the stored hashed password
  const passwordMatch = await comparePasswords(password, user.hashedPassword);
  if (!passwordMatch) {
    return null;
  }

  return user;
}

function generateUserId(): string {
  // Generate a unique user ID (you can use a library like UUID for this)
  // For simplicity, we'll just use a random number here
  return Math.random().toString(36).substr(2, 9);
}

export { register, login };
