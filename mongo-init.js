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

db.user.insert({
  name: "Pepe",
  last_name: " Argento",
  password: "password",
  email: "pepeargento@gmail.com",
  type: "CUSTOMER"
})
