package com.user.contoller;


import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.user.Model.Role;
import com.user.Model.Users;
import com.user.Utils.jwt;
import com.user.services.UserService;

import io.jsonwebtoken.Claims;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;



@RestController
@RequestMapping("/user")
public class userController {
    @Autowired
    private UserService UserService;
    
    @Autowired
    private jwt jwt;


    @PostMapping("/signup")
    public ResponseEntity<?> register(@RequestBody Users user){
        System.out.println("req mapped");
        try {
            Role role = Role.valueOf(user.getRole().toString());
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body("Invalid role. Allowed values are: " + Arrays.toString(Role.values()));
        }
        if(UserService.findByUsername(user.getUserName())!=null){
            return ResponseEntity.badRequest().body("Username already exists");
        }
        if (UserService.findByEmail(user.getEmail()) != null) {
            return ResponseEntity.badRequest().body("Email already exists");
        }
        Users registeredUser=UserService.register(user);
        return ResponseEntity.ok(registeredUser);
        
    };

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody Users loginRequest){
        Users user = UserService.findByUsername(loginRequest.getUserName());
        if (user == null || !UserService.checkPassword(loginRequest.getPassword(),loginRequest.getUserName())) {
            return ResponseEntity.status(401).body("Invalid credentials");
        }

        String token = jwt.generateToken(user.getUserName(), user.getRole());
        return ResponseEntity.ok(Map.of("token", token));

    }

    @PostMapping("/auth/validate")
    public ResponseEntity<?> validateToken(@RequestHeader("Authorization") String token) {
        if (token == null || !jwt.isTokenValid(token.replace("Bearer ", ""))) {
            return ResponseEntity.status(401).body("Invalid or expired token");
        }

        String username = jwt.extractUsername(token.replace("Bearer ", ""));
        String role = jwt.extractRole(token.replace("Bearer ", ""));
        return ResponseEntity.ok(Map.of("username", username, "role", role));
    }


    @GetMapping("/{id}")
    public ResponseEntity<?> getuser(@PathVariable UUID id){
        Users user= UserService.getUser(id).get();
        if(user==null){
            return ResponseEntity.status(404).body("User not Found");
        }
        return ResponseEntity.ok(user);
    }

    @GetMapping("/profile")
    public ResponseEntity<?> getProfile(@RequestHeader("Authorization") String token) {
        if (token == null || !jwt.isTokenValid(token.replace("Bearer ", ""))) {
            return ResponseEntity.status(401).body("Invalid or expired token");
        }

        String username = jwt.extractUsername(token.replace("Bearer ", ""));
        Claims claims = jwt.extractClaims(token.replace("Bearer ", ""));
        System.out.println(claims);
        return ResponseEntity.ok(UserService.findByUsername(username));
    }

    @DeleteMapping("/delete")
    public ResponseEntity<?> logout(@RequestHeader("Authorization") String token) {
        if(token==null || !jwt.isTokenValid(token.replace("Bearer", ""))){
            return ResponseEntity.status(401).body("Invalid or expired token");
        }
        String username=jwt.extractUsername(token.replace("Bearer", ""));
        UUID id=UserService.findByUsername(username).getId();
        Users deleted=UserService.deleteUser(id);
        return ResponseEntity.ok(deleted);
    }

    @PostMapping("/logout")
    public ResponseEntity<?> postMethodName(@RequestHeader("Authorization") String token) {
        if(token==null || !jwt.isTokenValid(token.replace("Bearer", ""))){
            return ResponseEntity.status(401).body("Invalid or expired token");
        }
        jwt.invalidateToken(token.replace("Bearer ", ""));
        return ResponseEntity.ok("User logged out successfully");
    }
    
    
    
    
}
