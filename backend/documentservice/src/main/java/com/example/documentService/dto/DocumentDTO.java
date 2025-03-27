package com.example.documentService.dto;

import com.example.documentService.Models.User;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.GenericGenerator;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DocumentDTO {

    private UUID id;
    private String name;
    private String filePath;
    private String userGivenName;
    private String type;
    private String username;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

}
