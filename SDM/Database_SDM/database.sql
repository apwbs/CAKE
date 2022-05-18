CREATE TABLE ciphertext (  
    sender_address TEXT,
    recipient_address TEXT,
    ipfs_hash TEXT,
    case_id TEXT,
    primary key (sender_address, ipfs_hash)
);

