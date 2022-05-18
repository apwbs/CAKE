CREATE TABLE pkmk_keys (
    recipient_address TEXT,
    pk TEXT,
    mk TEXT,
    primary key (recipient_address, pk, mk)
);

