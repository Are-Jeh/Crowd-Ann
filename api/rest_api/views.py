from django.shortcuts import render, HttpResponse
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework import views
from .serializers import ImageSerializer, AnnotationSerializer
from .models import Image, Annotation
from scipy.spatial import distance
from rest_framework  import permissions, authentication
from django.views.decorators.csrf import csrf_exempt
import json
import requests

# def scale_image( height, width, canvas_size,x,y):
#     origin      =(canvas_size[0][0],canvas_size[0][1], 0)
#     right_bottom=(canvas_size[1][0], canvas_size[1][1], 0)
#     left_top    =(canvas_size[2][0],canvas_size[2][1], 0)
        
#     length_str=distance.euclidean(origin,right_bottom)/width
#     width_str=distance.euclidean(origin,left_top)/height
        
#     actual_x=(distance.euclidean(origin,x)/length_str)
#     actual_y=(distance.euclidean(origin,y)/width_str)
        
#     return actual_x,actual_y

class ImageView(views.APIView):
    model = Image, Annotation
    serializer = ImageSerializer, AnnotationSerializer
    
    def get(self, request):
        id = int(request.GET.get('id'))
        token = request.GET.get('token')
        r = requests.post('http://localhost:8080/api/token/', json={"token": token})
        user_data = r.json()
        if user_data['status']:
            images = Image.objects.exclude(image_id__in = Annotation.objects.values('image_id'))
            serializer = ImageSerializer(data =images, many= True)
            serializer.is_valid()
            list_size = images.count()
            if id >= list_size:
                return JsonResponse({'status' : False}, safe=False)
            return JsonResponse(serializer.data[id], safe=False)
        else:
            return HttpResponseForbidden()
         
class AnnotationView(views.APIView):
    model = Image, Annotation
    serializer = ImageSerializer, AnnotationSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.RemoteUserAuthentication]

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            post_data = request.data
            result ={}
            token = post_data['token']
            print(token)
            r = requests.post('http://localhost:8080/api/token/', json={"token": token})
            user_data = r.json()
            if user_data['status']:
                try:
                    # post_data = json.loads(request.body.decode("utf-8"))
                    # print(post_data)
                    if post_data == '':
                        print("No Data Provided")
                    result = {}
                
                    # r = requests.post('http://localhost:8080', json={"token": "123456"})
                    x_cor = post_data['x_cor']
                    y_cor = post_data['y_cor']
                    images = Image.objects.get(pk=post_data['image_id'])
                    new_annotation = Annotation()
                    new_annotation.image_id = images
                    new_annotation.label = post_data['label']
                    new_annotation.user = user_data['email']
                    new_annotation.coordinates_x = x_cor
                    new_annotation.coordinates_y = y_cor
                    new_annotation.save()
                    result['status'] = True
                    return JsonResponse(result, safe=False)
                except:
                    result['status'] = False
                    return JsonResponse(result, safe=False)
            else:
                return HttpResponseForbidden()

class RetrieveAnnotationView(views.APIView):
    model = Image, Annotation
    serializer = AnnotationSerializer
    
    def get(self, request):
        
        post_data = request.GET.get('id')
        print(post_data)
        image_id = post_data
        annotation = Annotation.objects.filter(image_id_id = image_id)
        serializer = AnnotationSerializer(data=annotation, many= True, context={'request': request})
        serializer.is_valid()
        # print(serializer.data)
        return JsonResponse(serializer.data, safe=False)
      
      
class RetrieveImageView(views.APIView):
    model = Image, Annotation
    serializer = ImageSerializer
    
    def get(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(data =images, many= True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)
    