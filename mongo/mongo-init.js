db.createUser({
    user: 'app_user',
    pwd: 'test123',
    roles: [
      {
        role: 'dbOwner',
        db: 'project_db',
      },
    ],
  });