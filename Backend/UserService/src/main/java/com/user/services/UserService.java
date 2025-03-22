package com.user.services;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import com.user.Model.Users;

public interface UserService {
        Users register(Users user);

        Users findByUsername(String username);

        List<Users> getUsers();

        Optional<Users> getUser(UUID id);

        Users deleteUser(UUID userId);
        
        boolean checkPassword(String password, String username);

        Object findByEmail(String email);

}
