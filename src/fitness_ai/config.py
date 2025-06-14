"""
Configuration Management for Fitness AI System

Handles environment variables, model settings, and system configuration.
"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class FitnessAIConfig:
    """Configuration class for Fitness AI system."""
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.1
    openai_max_tokens: int = 1000
    
    # LangSmith Configuration
    langchain_tracing_v2: bool = True
    langchain_endpoint: str = "https://api.smith.langchain.com"
    langchain_api_key: Optional[str] = None
    langchain_project: str = "fitness-ai-orchestration"
    
    # System Configuration
    debug_mode: bool = False
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls) -> "FitnessAIConfig":
        """Create configuration from environment variables."""
        
        # Required OpenAI API key
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables! "
                "Please set it in your .env file or environment."
            )
        
        return cls(
            # OpenAI settings
            openai_api_key=openai_api_key,
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            openai_temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.1")),
            openai_max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1000")),
            
            # LangSmith settings
            langchain_tracing_v2=os.getenv("LANGCHAIN_TRACING_V2", "true").lower() == "true",
            langchain_endpoint=os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"),
            langchain_api_key=os.getenv("LANGCHAIN_API_KEY"),
            langchain_project=os.getenv("LANGCHAIN_PROJECT", "fitness-ai-orchestration"),
            
            # System settings
            debug_mode=os.getenv("DEBUG_MODE", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO").upper()
        )
    
    def validate(self) -> None:
        """Validate configuration settings."""
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
        
        if self.openai_temperature < 0 or self.openai_temperature > 1:
            raise ValueError("OpenAI temperature must be between 0 and 1")
        
        if self.openai_max_tokens < 1:
            raise ValueError("OpenAI max tokens must be positive")
        
        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(f"Invalid log level: {self.log_level}")
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return {
            "openai_model": self.openai_model,
            "openai_temperature": self.openai_temperature,
            "openai_max_tokens": self.openai_max_tokens,
            "langchain_tracing_v2": self.langchain_tracing_v2,
            "langchain_project": self.langchain_project,
            "debug_mode": self.debug_mode,
            "log_level": self.log_level
        }
    
    def __repr__(self) -> str:
        """String representation hiding sensitive data."""
        return (
            f"FitnessAIConfig("
            f"model={self.openai_model}, "
            f"temperature={self.openai_temperature}, "
            f"tracing={self.langchain_tracing_v2}, "
            f"project={self.langchain_project})"
        )


# Global configuration instance
config = FitnessAIConfig.from_env()
config.validate() 