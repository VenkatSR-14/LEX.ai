package com.example.documentService.service.impl;


import com.example.documentService.Models.Document;
import com.example.documentService.Models.User;
import com.example.documentService.dto.DocumentDTO;
import com.example.documentService.exception.DocumentNotFoundException;
import com.example.documentService.exception.ParserException;
import com.example.documentService.parser.factory.ParserFactory;
import com.example.documentService.parser.interfaces.DocumentParser;
import com.example.documentService.respository.DocumentRepository;
import com.example.documentService.service.interfaces.IDocumentService;
import com.example.documentService.service.interfaces.IUserService;
import lombok.RequiredArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.ui.ModelMap;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class DocumentServiceImpl implements IDocumentService {
    private final DocumentRepository documentRepository;
    private final IUserService userService;
    private final ParserFactory parserFactory;
    private final ModelMapper modelMapper;

    @Value("${document.upload.dir}")
    private String uploadDir;

    @Override
    public DocumentDTO uploadDocument(MultipartFile file, UUID userId) throws IOException{
        User user = userService.getUserEntityById(userId);
        String originalFileName = file.getOriginalFilename();
        String fileExtension = getFileExtension(originalFileName);
        String uniqueFileName = UUID.randomUUID() + "." + fileExtension;

        Path uploadPath = Paths.get(uploadDir);
        if (!Files.exists(uploadPath)){
            Files.createDirectories(uploadPath);
        }

        Path filePath = uploadPath.resolve(uniqueFileName);
        Files.copy(file.getInputStream(), filePath);

        Document document = new Document();
        document.setName(originalFileName);
        document.setType(fileExtension);
        document.setFilePath(filePath.toString());
        document.setUser(user);

        Document savedDocument = documentRepository.save(document);
        return modelMapper.map(savedDocument, DocumentDTO.class);
    }

    @Override
    public DocumentDTO getDocumentById(UUID id){
        Document document = documentRepository.findById(id).
                orElseThrow(() -> new DocumentNotFoundException("Document not found with id: "+ id));
        return modelMapper.map(document, DocumentDTO.class);
    }

    @Override
    public List<DocumentDTO> getDocumentsByUserId(UUID userId) {
        List<Document> documents = documentRepository.findByUserId(userId);
        return documents.stream()
                .map(doc -> modelMapper.map(doc, DocumentDTO.class))
                .collect(Collectors.toList());
    }

    @Override
    public String parseDocument(UUID id) throws Exception{
        Document document = documentRepository.findById(id).
                orElseThrow(() -> new DocumentNotFoundException("Document not found with id: " + id));

        DocumentParser parser = parserFactory.getParser(document.getType());
        Path filePath = Paths.get(document.getFilePath());

        try(var inputStream = Files.newInputStream(filePath)){
            return parser.parse(inputStream);
        }
        catch (Exception e){
            throw new ParserException("Error parsing document: " + e.getMessage(), e);
        }
    }

    @Override
    public void deleteDocument(UUID id) {
        Document document = documentRepository.findById(id)
                .orElseThrow(() -> new DocumentNotFoundException("Document not found with id: " + id));

        Path filePath = Paths.get(document.getFilePath());
        try {
            Files.deleteIfExists(filePath);
        } catch (IOException e) {
            // Log the error but continue with database deletion
            e.printStackTrace();
        }

        documentRepository.delete(document);
    }

    @Override
    public List<DocumentDTO> getAllDocuments(){
        List<Document> documents = documentRepository.findAll();
        return documents.stream()
                .map(doc -> modelMapper.map(doc, DocumentDTO.class))
                .collect(Collectors.toList());
    }

    @Override
    public DocumentDTO updateDocument(UUID id, DocumentDTO documentDTO){
        Document document = documentRepository.findById(id).
                orElseThrow(() -> new DocumentNotFoundException("Document not found with id: "+ id));

        document.setName(documentDTO.getName());
        Document updatedDocument = documentRepository.save(document);
        return modelMapper.map(updatedDocument, DocumentDTO.class);
    }

    private String getFileExtension(String fileName){
        return fileName.substring(fileName.lastIndexOf(".") + 1);
    }
}
