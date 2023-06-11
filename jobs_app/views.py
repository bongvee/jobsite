from django.shortcuts import render, get_object_or_404
from rest_framework import status                   # search statistics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
from django.db.models import Avg, Min, Max, Count   # search statistics
from .filters import JobsFilter


# read list of jobs
@api_view(['GET'])
def readAllJobs(request):

    # read all jobs
    # jobs = Job.objects.all()
    # serializer = JobSerializer(jobs, many=True)

    # read FILTERED jobs
    filterset = JobsFilter(request.GET, queryset=Job.objects.all().order_by('id'))
    serializer = JobSerializer(filterset.qs, many=True)

    return Response(serializer.data)


# read a specific job id
@api_view(['GET'])
def readAJob(request, pk):
    # to handle record/detail not found
    job = get_object_or_404(Job, id=pk)

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


# create/ add a new job
@api_view(['POST'])
def createAJob(request):
    data = request.data

    job = Job.objects.create(**data)

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


# update/ edit the job details
@api_view(['PUT'])
def updateAJob(request, pk):
    job = get_object_or_404(Job, id=pk)

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
def deleteAJob(request, pk):
    job = get_object_or_404(Job, id=pk)

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
