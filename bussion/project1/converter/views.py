import csv
import os.path
import uuid
from django.conf import settings
from google_currency import convert
from django.shortcuts import render
from .models import Company,MoneyConverter
from .serializers import CompanySerializer,MoneyConverterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
import pandas as pd
from openpyxl import Workbook,load_workbook
import openpyxl
from pathlib import Path
import json
from django.http import HttpResponseRedirect
from threading import Thread

class CompanyDeatil(viewsets.ViewSet):
    def retrieve(self,request,pk):
        try:
           std = MoneyConverter.objects.filter(company_id=pk)
        except MoneyConverter.DoesNotExist:
            return Response({"msg":"record not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = MoneyConverterSerializer(std,many=True)

        df =pd.DataFrame(serializer.data)
        a1 = f"media/{uuid.uuid4()}.csv"
        l1=a1.split("/")
        df.to_csv(a1,index=False,encoding="UTF-8",columns=['name', 'currency_name','amount','Date','converted_currency','converted_amount'])
        # print(os.path.join(settings.MEDIA_ROOT,l1[1]))
        urlfile="http://127.0.0.1:8000/"+a1
        response = {
            "data1":serializer.data,
            "file":urlfile
        }
        return Response(response,status=status.HTTP_200_OK)



    def create(self,request):
        serializer = CompanySerializer(data=request.data)
        converted_currency = request.POST.get("currency_name")
        file_id = request.POST.get("id")
        file1 = request.FILES.get("file1")

        if str(file1).endswith(".xlsx") == True or str(file1).endswith(".xlsm"):
            excel_data = pd.read_excel(file1)
            print(excel_data)
            # file_data= pd.DataFrame(excel_data, columns=['Name', 'Currency', "Amount","Transaction Date"])
            file_data= excel_data
            # df1 = file_data[file_data['Currency'] == "currency_name"]
            # print(df1)
        elif str(file1).endswith(".csv") == True:
               file_data = pd.read_csv(file1)


        if serializer.is_valid():
            serializer.save()
            def same():
                df1 = file_data[file_data['Currency'] == converted_currency]
                company_name = df1['Name'].tolist()
                currency_name = df1['Currency'].tolist()
                currency_amount = df1['Amount'].tolist()
                date_transaction = df1['Transaction Date'].tolist()
                for (company_name, currency_name, currency_amount, date_transaction) in zip(company_name, currency_name, currency_amount, date_transaction):
                        reg = MoneyConverter(company_id=file_id, name=company_name, currency_name=currency_name, amount=currency_amount, Date=date_transaction,
                                             converted_currency=converted_currency, converted_amount=currency_amount)
                        reg.save()
                        print("save")

            def diffrent():
                df1 = file_data[file_data['Currency'] != converted_currency]
                company_name = df1['Name'].tolist()
                currency_name = df1['Currency'].tolist()
                currency_amount = df1['Amount'].tolist()
                date_transaction = df1['Transaction Date'].tolist()
                for (company_name, currency_name, currency_amount, date_transaction) in zip(company_name, currency_name, currency_amount, date_transaction):
                    f = convert(currency_name,converted_currency, currency_amount)
                    print(f)
                    y = json.loads(f)
                    h = y["amount"]

                    reg = MoneyConverter(company_id=file_id, name=company_name, currency_name=currency_name, amount=currency_amount, Date=date_transaction, converted_currency=converted_currency,
                                         converted_amount=h)
                    reg.save()

            t1 = Thread(target=same)
            t2 = Thread(target=diffrent)
            t1.start()
            t2.start()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        """Another way"""

            # company_name = file_data['Name'].tolist()
            # currency_name = file_data['Currency'].tolist()
            # currency_amount = file_data['Amount'].tolist()
            # date_transaction = file_data['Transaction Date'].tolist()
            #
            # for (company_name, currency_name, currency_amount,date_transaction) in zip(company_name, currency_name, currency_amount,date_transaction):
            #     if converted_currency==currency_name:
            #         reg = MoneyConverter(company_id=file_id, name=company_name, currency_name=currency_name, amount=currency_amount, Date=date_transaction,
            #                              converted_currency=converted_currency, converted_amount=date_transaction)
            #         reg.save()
            #         print("save")
            #     else:
            #         f = convert(currency_name,converted_currency,currency_amount)
            #         print(f)
            #         y = json.loads(f)
            #         h=y["amount"]
            #
            #         reg = MoneyConverter(company_id=file_id,name=company_name,currency_name=currency_name,amount=currency_amount,Date=date_transaction,converted_currency=converted_currency,converted_amount=h)
            #         reg.save()
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
            # return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/company/std/'+file_id)
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
