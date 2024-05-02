import bcrypt from 'bcrypt';
import { HashedPassword } from '../interfaces/HashedPassword';

async function hashPassword(password: string): Promise<HashedPassword> {
  const saltRounds = 10;
  const hashedValue = await bcrypt.hash(password, saltRounds);

  return {
    algorithm: 'bcrypt',
    hashedValue,
    salt: '',
    iterations: saltRounds,
  };
}

async function comparePasswords(password: string, hashedPassword: HashedPassword): Promise<boolean> {
  return bcrypt.compare(password, hashedPassword.hashedValue);
}

export { hashPassword, comparePasswords };
