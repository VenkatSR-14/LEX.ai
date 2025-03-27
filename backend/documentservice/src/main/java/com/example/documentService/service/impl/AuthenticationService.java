package com.example.documentService.service.impl;

import com.example.documentService.Models.User;
import com.example.documentService.dto.AuthRequest;
import com.example.documentService.dto.AuthResponse;
import com.example.documentService.respository.UserRepository;
import com.example.documentService.security.JwtUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthenticationService {

    private final AuthenticationManager authenticationManager;
    private final UserServiceImpl userService;
    private final UserRepository userRepository;
    private final JwtUtil jwtUtil;

    public AuthResponse authenticate(AuthRequest authRequest) {
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(authRequest.getUserName(), authRequest.getPassword())
        );

        final UserDetails userDetails = userService.loadUserByUsername(authRequest.getUserName());
        final String jwt = jwtUtil.generateToken(userDetails);

        User user = userRepository.findByUsername(authRequest.getUserName()).orElseThrow();

        return new AuthResponse(jwt, user.getUsername(), user.getId().toString());
    }
}

