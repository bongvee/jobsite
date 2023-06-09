from django.shortcuts import render, get_object_or_404
from .models import Job

from rest_framework.decorators import api_view, permission_classes  # required JWT for CRUD
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated              # required JWT for CRUD
from rest_framework.pagination import PageNumberPagination  # Pagination
from rest_framework import status                           # search statistics
from django.db.models import Avg, Min, Max, Count           # search statistics

from .serializers import JobSerializer
from .filters import JobsFilter


# read list of jobs (public)
@api_view(['GET'])
def readAllJobs(request):

    # read all jobs
    # jobs = Job.objects.all()
    # serializer = JobSerializer(jobs, many=True)

    # read FILTERED jobs
    # filterset = JobsFilter(request.GET, queryset=Job.objects.all().order_by('id'))
    # serializer = JobSerializer(filterset.qs, many=True)
    # return Response(serializer.data)

    # read FILTERED jobs with PAGINATION
    filterset = JobsFilter(request.GET, queryset=Job.objects.all().order_by('id'))
    resultCount = filterset.qs.count()
    resultPerPage = 3
    paginator = PageNumberPagination()
    paginator.page_size = resultPerPage
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = JobSerializer(queryset, many=True)
    return Response({
        'resultCount': resultCount,
        'resultPerPage': resultPerPage,
        'jobs': serializer.data
    })

# read a specific job id
@api_view(['GET'])
@permission_classes([IsAuthenticated])      # required JWT for CRUD
def readAJob(request, pk):
    # to handle record/detail not found
    job = get_object_or_404(Job, id=pk)

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


# create/ add a new job
@api_view(['POST'])
@permission_classes([IsAuthenticated])      # required JWT for CRUD
def createAJob(request):
    request.data['user'] = request.user     # required JWT for CRUD
    data = request.data

    job = Job.objects.create(**data)

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


# update/ edit the job details
@api_view(['PUT'])
@permission_classes([IsAuthenticated])      # required JWT for CRUD
def updateAJob(request, pk):
    job = get_object_or_404(Job, id=pk)

    # required JWT for CRUD
    if job.user != request.user:
        return Response({ 'message': 'You\'re not allowed to update this job.' }, status=status.HTTP_403_FORBIDDEN)

    job.title = request.data['title']
    job.description = request.data['description']
    job.email = request.data['email']
    job.address = request.data['address']
    job.jobType = request.data['jobType']
    job.education = request.data['education']
    job.industry = request.data['industry']
    job.experience = request.data['experience']
    job.salary = request.data['salary']
    job.positions = request.data['positions']
    job.company = request.data['company']

    job.save()

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


# delete/ remove a job
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])      # required JWT for CRUD
def deleteAJob(request, pk):
    job = get_object_or_404(Job, id=pk)

    # required JWT for CRUD
    if job.user != request.user:
        return Response({ 'message': 'You\'re not allowed to delete this job.' }, status=status.HTTP_403_FORBIDDEN)

    job.delete()

    return Response({ 'message': 'The job is DELETED.' }, status=status.HTTP_200_OK)


# search statistics
@api_view(['GET'])
def readTopicStatistics(request, topic):

    args = { 'title__icontains': topic }
    jobs = Job.objects.filter(**args)

    if len(jobs) == 0:
        return Response({'message': 'No jobs found for {topic}'.format(topic=topic.upper())})
    
    status = jobs.aggregate(
        total_jobs= Count('title'),
        avg_salary = Avg('salary'),
        min_salary = Min('salary'),
        max_salary = Max('salary'),
    )

    return Response(status)
