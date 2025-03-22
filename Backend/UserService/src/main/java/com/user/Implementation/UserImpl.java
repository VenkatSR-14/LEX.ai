package com.user.Implementation;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.user.Model.Users;
import com.user.Repo.UserRepo;
import com.user.Utils.Config;
import com.user.services.UserService;

import jakarta.persistence.EntityNotFoundException;

@Service
public class UserImpl implements UserService {

    @Autowired
    private UserRepo userRepo;

    @Autowired
    private Config config;
    

    @Override
    public List<Users> getUsers() {
        return userRepo.findAll();
    }

    @Override
    public Optional<Users> getUser(UUID id) {
        return userRepo.findById(id);
    }

    // @Override
    // public void editUser(UUID userId, Users updatedUser) {
    //     // TODO Auto-generated method stub
    //     throw new UnsupportedOperationException("Unimplemented method 'editUser'");
    // }

    @Override
public Users deleteUser(UUID userId) {
    Optional<Users> userOptional = userRepo.findById(userId);
    if (userOptional.isPresent()) {
        Users user = userOptional.get();
        userRepo.delete(user); 
        return user; 
    } else {
        throw new EntityNotFoundException("User with ID " + userId + " not found.");
    }
}
    @Override
    public Users register(Users user) {
        user.setPassword(config.passwordEncoder().encode(user.getPassword()));
        return userRepo.save(user);
    }

    @Override
    public Users findByUsername(String username) {
        return userRepo.findByuserName(username);
    }

    @Override
    public boolean checkPassword(String password, String username) {
        return config.passwordEncoder().matches(password,findByUsername(username).getPassword());
    }

    @Override
    public Object findByEmail(String email) {
        return userRepo.findByEmail(email);
    }

}
