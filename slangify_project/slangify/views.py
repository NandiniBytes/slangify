from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Slang, Category
from .serializers import SlangSerializer, CategorySerializer
import vertexai
from vertexai.generative_models import GenerativeModel
from django.conf import settings
import random

# Initialize Vertex AI
try:
    vertexai.init(project=settings.GEMINI_PROJECT_ID, location=settings.GEMINI_LOCATION)
except Exception as e:
    print(f"Failed to initialize Vertex AI: {str(e)}")

class SlangViewSet(viewsets.ModelViewSet):
    queryset = Slang.objects.all()
    serializer_class = SlangSerializer

    def get_object(self):
        term = self.kwargs.get('pk')
        try:
            # Case-insensitive lookup in the database
            slang = Slang.objects.get(term__iexact=term)
            return slang
        except Slang.DoesNotExist:
            # Term not found in database, fall back to Gemini API
            try:
                model = GenerativeModel("gemini-2.0-flash-001")  # Updated model name
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
                    "created_at": "2025-06-03T10:37:00+05:30",
                    "usage_example": "N/A",
                    "cultural_origin": "N/A",
                    "trendiness_score": 0
                }
                return mock_slang
            except Exception as e:
                raise NotFound(detail=f"Slang not found and Gemini API failed: {str(e)}")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if isinstance(instance, Slang):
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            # If it's a mock object from Gemini, return it directly
            return Response(instance)

    @action(detail=False, methods=['get'])
    def slang_of_the_day(self, request):
        try:
            slang = random.choice(self.get_queryset())
            serializer = self.get_serializer(slang)
            slang_data = serializer.data

            # Generate context using Gemini API
            try:
                model = GenerativeModel("gemini-1.5-flash-001")  # Updated model name
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
            except Exception as e:
                slang_data["generated_context"] = f"Could not generate context: {str(e)}"

            return Response(slang_data)
        except IndexError:
            return Response({"error": "No slangs available in the database."}, status=404)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
