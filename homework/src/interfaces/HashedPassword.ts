interface HashedPassword {
  algorithm: string;
  hashedValue: string;
  salt: string;
  iterations: number;
}

export { HashedPassword };
