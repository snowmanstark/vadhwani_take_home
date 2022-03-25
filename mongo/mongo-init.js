db.createUser({
    user: 'app_user_1278',
    pwd: 'test123',
    roles: [
      {
        role: 'dbOwner',
        db: 'project_db',
      },
    ],
  });