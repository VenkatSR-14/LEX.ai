package com.user.Utils;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.user.Model.Role;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;

@Component
public class jwt {

    @Autowired
    private KeyProvider keyProvider;

    // private static final String SECRET_KEY = "2D4A614E645267556B58703273357638792F423F4428472B4B6250655368566D";
    private static final long EXPIRATION_TIME = 1000 * 60 * 60; 

    @SuppressWarnings("deprecation")
    public String generateToken(String username,Role role){
        Map<String,Object> claims =new HashMap<>();
        claims.put("role",role);

        return Jwts.builder()
        .setClaims(claims)
        .setSubject(username)
        .setIssuedAt(new Date(System.currentTimeMillis()))
        .setExpiration(new Date(System.currentTimeMillis()+EXPIRATION_TIME))
        .signWith(SignatureAlgorithm.HS256,keyProvider.getSecretKey())
        .compact();
    }

    @SuppressWarnings("deprecation")
    public Claims extractClaims(String token) {
        return Jwts.parser()
                .setSigningKey(keyProvider.getSecretKey())
                .parseClaimsJws(token)
                .getBody();
    }

    public String extractUsername(String token) {
        return extractClaims(token).getSubject();
    }

    public String extractRole(String token) {
        return (String) extractClaims(token).get("role");
    }

    public boolean isTokenValid(String token) {
        try{
        return extractClaims(token).getExpiration().after(new Date());
        }
        catch(Exception err){
            return false;
        }
    }

    public void invalidateToken(String token) {
        String newSecretKey = keyProvider.generateNewSecretKey();
        keyProvider.setSecretKey(newSecretKey);
        System.out.println("All tokens invalidated by updating the secret key.");
    }

}
