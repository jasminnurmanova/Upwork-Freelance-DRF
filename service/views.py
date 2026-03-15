from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Project
from .serializers import ProjectSerializer
from user.models import Bid,Submission,Review,Contract
from user.serializers import BidSerializer,ContractSerializer,ReviewSerializer
from django.db import transaction

class ProjectCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        if request.user.role != "client":
            return Response(
                {"error": "Faqat client project yaratishi mumkin"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.client != request.user:
            return Response(
                {"error": "Ruxsat yo'q"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ProjectSerializer(project,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.client != request.user:
            return Response(
                {"error": "Ruxsat yo'q"},
                status=status.HTTP_403_FORBIDDEN
            )
        project.delete()
        return Response({"message": "Project o'chirildi"},status=status.HTTP_204_NO_CONTENT)

class MyProjectsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        projects = Project.objects.filter(client=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

class ProjectDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

class ProjectsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        projects = Project.objects.filter(status="open").order_by("-created_at")
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

#freelancerga
class BidCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        if request.user.role != "freelancer":
            return Response(
                {"error": "Faqat freelancer bid yubora oladi"},
                status=status.HTTP_403_FORBIDDEN
            )
        project = get_object_or_404(Project, pk=pk)
        if Bid.objects.filter(project=project, freelancer=request.user).exists():
            return Response({"error": "Siz bu projectga allaqachon bid yuborgansiz"},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = BidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                freelancer=request.user,
                project=project )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FreelancerBidListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        bids = Bid.objects.filter(freelancer=request.user).order_by("-created_at")
        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)

class BidDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        bid = get_object_or_404(Bid,pk=pk,freelancer=request.user)
        serializer = BidSerializer(bid)
        return Response(serializer.data)


class ProjectBidListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        bids = Bid.objects.filter(project=project)
        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)

class ClientBidListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        bids = Bid.objects.filter(project__client=request.user)
        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)

class AcceptBidView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, bid_id):
        bid = get_object_or_404(Bid, id=bid_id)
        project = bid.project
        if project.client != request.user:
            raise PermissionDenied("Faqat client bid qabul qila oladi")
        with transaction.atomic():
            bid.status = "accepted"
            bid.save()
            Bid.objects.filter(project=project)\
                .exclude(id=bid.id)\
                .update(status="rejected")
            project.status = "in_progress"
            project.save()
            contract = Contract.objects.create(
                project=project,
                client=project.client,
                freelancer=bid.freelancer,
                agreed_price=bid.price,
                status="active"
            )
        serializer = ContractSerializer(contract)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RejectBidView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, bid_id):
        bid = get_object_or_404(Bid, id=bid_id)
        project = bid.project
        if project.client != request.user:
            raise PermissionDenied("Faqat client bidni rad eta oladi")
        bid.status = "rejected"
        bid.save()
        serializer = BidSerializer(bid)
        return Response(serializer.data)

class ContractListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        contracts = Contract.objects.filter(
            client=request.user
        ) | Contract.objects.filter(
            freelancer=request.user
        )
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)

class ContractDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, contract_id):
        contract = get_object_or_404(Contract, id=contract_id)
        if request.user not in [contract.client, contract.freelancer]:
            raise PermissionDenied("Ruxsat yo‘q")
        serializer = ContractSerializer(contract)
        return Response(serializer.data)


class FinishContractView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, contract_id):
        contract = get_object_or_404(Contract, id=contract_id)
        if contract.client != request.user:
            raise PermissionDenied("Faqat client contractni tugata oladi")
        contract.status = "finished"
        contract.save()
        project = contract.project
        project.status = "completed"
        project.save()
        return Response(
            {"message": "Contract tugatildi"},
            status=status.HTTP_200_OK
        )

class ReviewCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, contract_id):
        contract = get_object_or_404(Contract, id=contract_id)
        if contract.client != request.user:
            raise PermissionDenied("Faqat client review yozishi mumkin")
        if hasattr(contract, "review"):
            return Response(
                {"error": "Bu contract uchun review allaqachon yozilgan"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(contract=contract)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
