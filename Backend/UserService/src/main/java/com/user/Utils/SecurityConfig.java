package com.user.Utils;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;


@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable()) // Disable CSRF if not needed
            .authorizeHttpRequests(authz -> authz
                // .requestMatchers("/user/signup", "/user/login", "/auth/**").permitAll() // Allow signup and login for unauthenticated users
                .anyRequest().permitAll() // Require authentication for other requests
            )
            .formLogin(form -> form.disable()) // Disable default form login
            .httpBasic(basic -> basic.disable()); // Disable HTTP Basic authentication

        return http.build();
    }

    // @Bean
    // public PasswordEncoder passwordEncoder() {
    //     return new BCryptPasswordEncoder(); // Use BCrypt for password encoding
    // }
}

