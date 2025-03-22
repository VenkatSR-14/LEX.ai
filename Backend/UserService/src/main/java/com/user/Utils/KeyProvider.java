package com.user.Utils;

import java.security.SecureRandom;
import java.util.Base64;


import org.springframework.stereotype.Component;

@Component
public class KeyProvider {
    private volatile String secretKey = "2D4A614E645267556B58703273357638792F423F4428472B4B6250655368566D";

    public String getSecretKey() {
        return secretKey;
    }

    public void setSecretKey(String newSecretKey) {
        this.secretKey = newSecretKey;
    }

    public String generateNewSecretKey() {
        byte[] key = new byte[32]; 
        SecureRandom secureRandom = new SecureRandom();
        secureRandom.nextBytes(key);
        return Base64.getEncoder().encodeToString(key);
    }
}
