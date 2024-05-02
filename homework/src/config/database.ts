import { User } from '../interfaces/User';

const users: User[] = [];

async function getUser(usernameOrEmail: string): Promise<User | undefined> {
  return users.find(user => user.username === usernameOrEmail || user.email === usernameOrEmail);
}

async function saveUser(user: User): Promise<void> {
  users.push(user);
}

export { getUser, saveUser };
