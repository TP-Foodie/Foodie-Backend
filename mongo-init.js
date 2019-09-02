db.createUser({
  user: 'app',
  pwd: 'password',
  roles: [
    {
      role: 'root',
      db: 'admin',
    },
  ],
});

db.users.insert({
  name: "Pepe Argento"
})