/*
  # Initial Schema Setup for AI Agency Management System

  1. New Tables
    - `users`
      - `id` (uuid, primary key)
      - `email` (text, unique)
      - `hashed_password` (text)
      - `company_name` (text)
      - `created_at` (timestamp)
    
    - `projects`
      - `id` (uuid, primary key)
      - `client_id` (uuid, foreign key to users)
      - `title` (text)
      - `description` (text)
      - `ai_service` (text)
      - `requirements` (text)
      - `status` (text)
      - `cost` (numeric)
      - `created_at` (timestamp)
      - `updated_at` (timestamp)

  2. Security
    - Enable RLS on both tables
    - Add policies for user authentication and data access
*/

-- Users table
CREATE TABLE users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email text UNIQUE NOT NULL,
    hashed_password text NOT NULL,
    company_name text NOT NULL,
    created_at timestamptz DEFAULT now()
);

-- Projects table
CREATE TABLE projects (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id uuid REFERENCES users(id),
    title text NOT NULL,
    description text,
    ai_service text NOT NULL,
    requirements text,
    status text NOT NULL DEFAULT 'pending',
    cost numeric DEFAULT 0,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Users policies
CREATE POLICY "Users can read own data"
    ON users
    FOR SELECT
    TO authenticated
    USING (auth.uid() = id);

-- Projects policies
CREATE POLICY "Clients can read own projects"
    ON projects
    FOR SELECT
    TO authenticated
    USING (client_id = auth.uid());

CREATE POLICY "Clients can create own projects"
    ON projects
    FOR INSERT
    TO authenticated
    WITH CHECK (client_id = auth.uid());

CREATE POLICY "Clients can update own projects"
    ON projects
    FOR UPDATE
    TO authenticated
    USING (client_id = auth.uid());