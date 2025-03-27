package com.example.documentService.service.interfaces;

import com.example.documentService.Models.User;
import com.example.documentService.dto.UserDTO;

import java.util.List;
import java.util.UUID;

public interface IUserService {
    UserDTO createUser(UserDTO userDTO);
    UserDTO getUserById(UUID id);
    UserDTO getUserByUsername (String username);
    List<UserDTO> getAllUsers();
    UserDTO updateUser(UUID id, UserDTO userDTO);
    void deleteUser(UUID id);
    User getUserEntityById(UUID id);
}
