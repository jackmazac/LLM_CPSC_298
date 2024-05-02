interface HashedPassword {
  algorithm: string;
  hashedValue: string;
}

interface User {
  id: string;
  username: string;
  email: string;
  hashedPassword: HashedPassword;
  createdAt: Date;
  updatedAt: Date;
}

export { User, HashedPassword };
