import * as bcrypt from 'bcrypt';

interface User {
    id: number;
    username: string;
    passwordHash: string;
  }
  
  interface LoginCredentials {
    username: string;
    password: string;
  }
  
  interface HashedPassword {
    hash: string;
  }


// This function simulates fetching a user from a database.
// In a real application, replace this with actual database retrieval logic.
async function findUserByUsername(username: string): Promise<User | undefined> {
  // Simulated database user retrieval
  // Remember to use parameterized queries to prevent SQL injection when implementing this for real
  return { id: 1, username: 'johnDoe', passwordHash: '$2b$10$examplehash...' }; // Example hashed password
}

// Hashes a password using bcrypt
async function hashPassword(password: string): Promise<HashedPassword> {
  const saltRounds = 10; // Adjust salt rounds as needed
  const hash = await bcrypt.hash(password, saltRounds);
  return { hash };
}

// Compares the password with the hashed password
async function comparePassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// Function to handle user login
async function loginUser(credentials: LoginCredentials): Promise<User | null> {
  const user = await findUserByUsername(credentials.username);
  if (!user) {
    console.log('User not found');
    return null; // User not found
  }

  const isPasswordCorrect = await comparePassword(credentials.password, user.passwordHash);
  if (!isPasswordCorrect) {
    console.log('Invalid password');
    return null; // Password incorrect
  }

  console.log('User logged in successfully');
  return user; // Successful login
}
