from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Slang, Category
from .serializers import SlangSerializer, CategorySerializer
import os
import random
import logging

# Set up logging
logger = logging.getLogger(__name__)

class SlangViewSet(viewsets.ModelViewSet):
    queryset = Slang.objects.all()
    serializer_class = SlangSerializer

    def list(self, request, *args, **kwargs):
        logger.debug("Entering SlangViewSet list method")
        try:
            logger.debug("Fetching queryset")
            queryset = self.get_queryset()
            logger.debug(f"Queryset fetched: {queryset}")
            if not queryset.exists():
                logger.debug("No slangs found, returning empty list")
                return Response([])
            logger.debug("Serializing queryset")
            serializer = self.get_serializer(queryset, many=True)
            logger.debug("Serialization complete, returning response")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in SlangViewSet list: {str(e)}", exc_info=True)
            raise

    def get_object(self):
        term = self.kwargs.get('pk')
        logger.debug(f"Fetching slang with term: {term}")
        try:
            # Case-insensitive lookup in the database
            slang = Slang.objects.get(term__iexact=term)
            return slang
        except Slang.DoesNotExist:
            # Term not found in database, fall back to Gemini API
            logger.debug(f"Slang '{term}' not found in database, querying Gemini API")
            try:
                import google.generativeai as genai
                genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                if not os.getenv("GOOGLE_API_KEY"):
                    raise ValueError("GOOGLE_API_KEY is not set")
                model = genai.GenerativeModel("gemini-2.0-flash")
                prompt = f"What does the slang term '{term}' mean? Provide a concise definition and, if possible, its origin or cultural context."
                response = model.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": 100,
                        "temperature": 0.7
                    }
                )
                generated_text = response.text

                # Create a mock Slang object for serialization
                mock_slang = {
                    "term": term,
                    "meaning": generated_text,
                    "category": {"id": None, "name": "Unknown", "description": "N/A"},
                    "origin": "Retrieved from Gemini API",
                    "popularity": 0,
                    "created_at": "2025-06-03T11:44:00+05:30",
                    "usage_example": "N/A",
                    "cultural_origin": "N/A",
                    "trendiness_score": 0
                }
                logger.debug(f"Gemini API response for '{term}': {mock_slang}")
                return mock_slang
            except ImportError as e:
                logger.error(f"Failed to import google.generativeai: {str(e)}")
                raise NotFound(detail="Slang not found in database and Gemini API is unavailable due to missing library")
            except Exception as e:
                logger.error(f"Error in Gemini API call: {str(e)}", exc_info=True)
                raise NotFound(detail=f"Slang not found and Gemini API failed: {str(e)}")

    def retrieve(self, request, *args, **kwargs):
        logger.debug("Entering SlangViewSet retrieve method")
        instance = self.get_object()
        if isinstance(instance, Slang):
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            # If it's a mock object from Gemini, return it directly
            return Response(instance)

    @action(detail=False, methods=['get'])
    def slang_of_the_day(self, request):
        logger.debug("Entering slang_of_the_day method")
        try:
            slang = random.choice(self.get_queryset())
            serializer = self.get_serializer(slang)
            slang_data = serializer.data

            # Generate context using Gemini API
            logger.debug("Generating context with Gemini API")
            try:
                import google.generativeai as genai
                genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                if not os.getenv("GOOGLE_API_KEY"):
                    raise ValueError("GOOGLE_API_KEY is not set")
                model = genai.GenerativeModel("gemini-2.0-flash")
                prompt = (
                    f"Generate a fun, casual sentence or short context using the Gen Z slang term '{slang.term}' "
                    f"which means '{slang.meaning}'. The sentence should reflect how a Gen Z person might use it on social media."
                )
                response = model.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": 50,
                        "temperature": 0.7
                    }
                )
                generated_text = response.text
                slang_data["generated_context"] = generated_text
                logger.debug(f"Generated context: {generated_text}")
            except ImportError as e:
                logger.error(f"Failed to import google.generativeai: {str(e)}")
                slang_data["generated_context"] = "Gemini API unavailable due to missing library"
            except Exception as e:
                logger.error(f"Error generating context with Gemini API: {str(e)}", exc_info=True)
                slang_data["generated_context"] = f"Could not generate context: {str(e)}"

            return Response(slang_data)
        except IndexError:
            logger.error("No slangs available in the database.")
            return Response({"error": "No slangs available in the database."}, status=404)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
