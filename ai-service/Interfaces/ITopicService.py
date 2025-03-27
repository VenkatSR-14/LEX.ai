from abc import ABC, abstractmethod

class ITopicService(ABC):
    
    """
    This will have An AI component with it. This is done using 
    Langchain
    """
    @abstractmethod
    def generate_content(self, topic_name, topic_description):
        pass

    """
    This will be used to mark the status of the topic
    Keep it as an enum: 0 => Not opened 1 => Opened 2 => Finished
    """
    @abstractmethod
    def change_topic_status(self, topic_id):
        pass