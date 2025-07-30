-- Database is already created by environment variables
-- Connect to the database
\c myapp;

-- Create items table if it doesn't exist
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on title for better performance
CREATE INDEX IF NOT EXISTS idx_items_title ON items(title);

-- Insert some sample data
INSERT INTO items (title, description) VALUES
    ('Sample Item 1', 'This is a sample item for testing'),
    ('Sample Item 2', 'Another sample item with description'),
    ('Sample Item 3', 'Third sample item for demonstration')
ON CONFLICT (id) DO NOTHING; 