package com.example.documentService.service.interfaces;

import com.example.documentService.Models.Document;
import com.example.documentService.dto.DocumentDTO;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.UUID;

public interface IDocumentService {
    DocumentDTO uploadDocument(MultipartFile file, UUID userId) throws IOException;
    DocumentDTO getDocumentById(UUID id);
    List<DocumentDTO> getDocumentsByUserId(UUID userId);
    String parseDocument(UUID id) throws Exception;
    void deleteDocument(UUID uuid);

    List<DocumentDTO> getAllDocuments();
    DocumentDTO updateDocument(UUID id, DocumentDTO documentDTO);
}
