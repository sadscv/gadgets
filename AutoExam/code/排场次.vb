Option Compare Database
Option Explicit
Option Base 1

Private Sub ���θ�λ_Click()
    CurrentDb.Execute ("update kcYrs set ���α�ʶ = 0")
If testTable("kcYrsԤ��") Then
    If CurrentData.AllTables("kcYrsԤ��").IsLoaded Then DoCmd.Close acTable, "kcYrsԤ��", acSaveNo
    CurrentDb.Execute ("UPDATE kcYrsԤ�� INNER JOIN kcYrs ON kcYrsԤ��.�γ̺� = kcYrs.�γ̺� SET kcYrs.���α�ʶ = [kcYrsԤ��].[���α�ʶ] " _
                    & "WHERE (((kcYrsԤ��.���α�ʶ)=True))")
End If
Me.kcQuery.Requery
End Sub

Private Sub ���Է�λ_Click()
CurrentDb.Execute ("update kcYrs set ������ = false where ������ = true")
Me.kcQuery.Requery
End Sub

Private Sub ȷ��_Click()
'**********************************************************************************************************************
'
'�ر���ʾ��
'һ���༶����"0000#1"������ĳ�ſγ̲�����������190�˵ģ�����"0000#2"����һ�룬ͬ�����оŰ��˾��������ƽ�֣�
'��������ͬ�γ̺Ų�ͬ�Ծ�ģ�һ��Ҫ�ò�ͬ�İ༶�ű�ǣ�������'0000#2'��
'����˫רҵ�Ŀγ̰༶����"24002093"��
'�ġ�Ҫ�ֿ�ʱ��Ŀγ̣�������Ҫ��������������ǰ�ڡ�kcYrs����ֺó��Σ�
'�塢��������ö����ı���Ϊϵͳ��Ľ��ұ�̫�����ˡ�
'
'**********************************************************************************************************************
DoCmd.Hourglass (True)
Dim sTime As Single '��ʱ��������������ĳ����εĺ�ʱ
Dim str As String
Dim l As Long
Dim i As Integer, j As Integer
Dim rs As DAO.Recordset
Dim tKs As Date
tKs = DLookup("ksxq", "Para") 'ȡ������ѧ��
'sTime = Timer

Dim iLoopCnt As Integer
iLoopCnt = 8

If testTable("xsYxk") Then
    '�жϸñ��Ƿ�򿪣�������ǿ�йرղ�ɾ��
    If CurrentData.AllTables("xsYxk").IsLoaded Then DoCmd.Close acTable, "xsYxk", acSaveNo
    CurrentDb.Execute ("drop table xsYxk")
End If

'����ѧ����ѡ���ӱ�--------�ȽϷ�ʱ
str = "SELECT ѧ����ѡ��.�γ̺�, ѧ����ѡ��.ѧ��, ѧ����ѡ��.�༶�� INTO xsYxk " _
& "FROM kcYrs INNER JOIN ((ѧ�� INNER JOIN ѧ����ѡ�� ON ѧ��.ѧ�� = ѧ����ѡ��.ѧ��) INNER JOIN �༶ ON ѧ��.�༶�� = �༶.�༶��) ON kcYrs.�γ̺� = ѧ����ѡ��.�γ̺� " _
& "WHERE (((ѧ����ѡ��.����ʱ��) = #" & tKs & "#) And ((ѧ����ѡ��.ѡ��״̬) = 0 Or (ѧ����ѡ��.ѡ��״̬) Is Null) And ((kcYrs.������) = False)) " _
& "ORDER BY ѧ����ѡ��.�γ̺�, ѧ����ѡ��.ѧ��"
CurrentDb.Execute (str)
CurrentDb.Execute ("alter table xsYxk add column ��� Byte")
CurrentDb.Execute ("update xsYxk set ���=1")

Dim iC As Integer '�ܹ�Ҫ�ſ��Ŀγ�����
Dim iPC As Integer '�ܹ�Ҫ�ſ��ķǹ�ѡ�����������γ̳̺�Ϊ��00*�Ŀγ�
Dim iiS As Integer '�ܹ�Ҫ�ſ���ѧ������

'�������ſ���ѧ������
str = "SELECT DISTINCT ѧ�� FROM xsYxk"
Set rs = CurrentDb.OpenRecordset(str)
rs.MoveLast
rs.MoveFirst

iiS = rs.RecordCount
iC = DCount("�γ̺�", "kcYrs", "������=false")
iPC = DCount("�γ̺�", "kcYrs", "������=false ") 'and �γ̺� not like '00*'

Dim C() As String '������Ҫ�ſ��Ŀγ̺�
ReDim C(iC)

Dim cPre() As Byte '����Ԥ�ŵĳ��α�ʶ
ReDim cPre(iC)

Dim cOK() As Byte '�γ����ŵĳ��α�ʶ
ReDim cOK(iC)

Dim S() As String '���ò���ѡ�ε�ѧ��ѧ��
ReDim S(iiS)

Dim cs() As Byte '����ѧ����ѡ�α�
ReDim cs(iC, iiS)

i = 1
'��ѧ�����鸳ֵ
Do While Not rs.EOF
    S(i) = Trim(rs("ѧ��"))
    rs.MoveNext
    i = i + 1
Loop

str = "select �γ̺� from kcYrs where ������=false order by ѡ������ desc"
Set rs = CurrentDb.OpenRecordset(str)
i = 1
'�Կγ����鸳ֵ
Do While Not rs.EOF
    C(i) = Trim(rs("�γ̺�"))
    rs.MoveNext
    i = i + 1
Loop

Set rs = CurrentDb.OpenRecordset("xsYxk")
Do While Not rs.EOF
'�Զ�ά���鸳ֵ--------�൱��ʱ--------�����Ժ�ö���
'    For i = 1 To iC
'        If Trim(rs("�γ̺�")) = c(i) Then
'            For j = 1 To iiS
'                If Trim(rs("ѧ��")) = s(j) Then
'                    cs(i, j) = 1
'                End If
'            Next j
'        End If
'    Next i

    i = GetSubscript(C(), Trim(rs("�γ̺�")))
    j = GetSubscript(S(), Trim(rs("ѧ��")))
    cs(i, j) = 1

    rs.MoveNext
Loop

rs.Close
Set rs = Nothing

'========================================================���¿�ʼ�ſ�����========================================================
'����רҵ�Σ��������ڲ�ͬ��ʱ����Ź�ѡ�Σ�����յ���
Dim iKcbs As Integer
Dim iMin As Integer
Dim k As Integer
Dim m As Integer
Dim n As Integer
Dim iPreMax As Integer 'Ԥ�ŵ���󳡴�
iPreMax = DMax("���α�ʶ", "kcYrs")

Dim iPreCount 'Ԥ�ŵĳ�����
iPreCount = DCount("*", "kcYrs", "���α�ʶ>0")

Dim iLoopCount As Integer '��ʱ����������ͳ�Ƹ���ʱ���ڵ��ſ�����


'�ȴ���Ԥ�ŵĿγ�'''''''''''''''''''''''''''''''''
For i = 1 To iC
    cPre(i) = DLookup("���α�ʶ", "kcYrs", "�γ̺�='" & C(i) & "'")
Next i
'������϶�Ԥ�ų�����ͬ�Ŀγ̽����ж��Ƿ��г�ͻ�Ĵ���

'���ŷǹ�ѡ��========================================================
Randomize
iMin = 32767
'Do While Timer - sTime < 7200
Do While iLoopCount < iLoopCnt
    iLoopCount = iLoopCount + 1

    '��������ݸ���ֵ��Ϊ��һ��ѭ����׼��
    iKcbs = 1 + iPreMax
    For k = 1 To iC
        cOK(k) = cPre(k)
    Next k

    For k = 1 To iPC - iPreCount '�������γ������һ����ѭ��
        n = Int(((iPC - iPreCount - k + 1) * Rnd) + 1)
        m = 0
        i = 1

        '�ҵ���n��δ�Ŷ��Ŀγ̵��±�i
        Do While m < n
            '��2009���ϰ��꿪ʼ���Թ�ѡ�ε�������
            If cOK(i) = 0 Then m = m + 1 'And Left(C(i), 2) <> "00"
            i = i + 1
        Loop
        i = i - 1

        For j = 1 To iC
            If cOK(j) <> 0 Then
                If MergeKc(C(), cs(), C(j), C(i)) = True Then '�ܺ���һʱ��εĵ�һ�ſγ̺ϲ�
                    For l = 1 To iC
                        If l <> j And cOK(l) = cOK(j) Then
                             If MergeKc(C(), cs(), C(l), C(i)) = False Then '�����ܺ���һʱ��ε������γ̺ϲ�
                                Exit For
                             End If
                        End If
                    Next l

                    If l = iC + 1 Then '�ܺ���һʱ��ε�ȫ���γ̺ϲ�
                        cOK(i) = cOK(j)
                        Exit For
                    End If
                End If

            End If
        Next j

        'ɨ��һ���û�ܺϲ������¿�һ��ʶ
        If j = iC + 1 Then
            cOK(i) = iKcbs
            iKcbs = iKcbs + 1
        End If
    Next k

    '�����һ��ѭ����õĳ���С����һ�Σ��򱣴���һ�εĽ��
    If iKcbs < iMin Then
        iMin = iKcbs
        For i = 1 To iC
            CurrentDb.Execute ("update kcYrs set ���α�ʶ=" & cOK(i) & " where �γ̺�='" & C(i) & "'")
        Next i
    End If

Loop

''MsgBox "������" & iLoopCount & "�ηǹ�ѡ��"
'iLoopCount = 0
'
''���Ź�ѡ��========================================================
''����ʱ���'����ʱ���'����ʱ���'����ʱ���'����ʱ���'����ʱ���'����ʱ���'����ʱ���
'Dim iLastKcbs As Integer
'iLastKcbs = DMax("���α�ʶ", "kcYrs") '�����ǹ�ѡ�ε��ſ�������
'iMin = 32767
'Do While iLoopCount < iLoopCnt
'    iLoopCount = iLoopCount + 1
'
'    '��������ݸ���ֵ��Ϊ��һ��ѭ����׼��
'    iKcbs = iLastKcbs + 1
'    For k = 1 To iC
'        If Left(C(k), 2) = "00" Then cOK(k) = 0
'    Next k
'
'    For k = 1 To iC - iPC '��������ѡ�γ������һ����ѭ��
'        n = Int(((iC - iPC - k + 1) * Rnd) + 1)
'        m = 0
'        i = 1
'
'        '�ҵ���n��δ�Ŷ��Ŀγ̵��±�i
'        Do While m < n
'            If cOK(i) = 0 And Left(C(i), 2) = "00" Then m = m + 1
'            i = i + 1
'        Loop
'        i = i - 1
'
'        For j = 1 To iC
'            If cOK(j) <> 0 And Left(C(j), 2) = "00" Then '+++++++++++++++++++++++++++++++++++
'                If MergeKc(C(), cs(), C(j), C(i)) = True Then '�ܺ���һʱ��εĵ�һ�ſγ̺ϲ�
'                    For l = 1 To iC
'                        If l <> j And cOK(l) = cOK(j) Then
'                             If MergeKc(C(), cs(), C(l), C(i)) = False Then '�����ܺ���һʱ��ε������γ̺ϲ�
'                                Exit For
'                             End If
'                        End If
'                    Next l
'
'                    If l = iC + 1 Then '�ܺ���һʱ��ε�ȫ���γ̺ϲ�
'                        cOK(i) = cOK(j)
'                        Exit For
'                    End If
'                End If
'
'            End If
'        Next j
'
'        'ɨ��һ���û�ܺϲ������¿�һ��ʶ
'        If j = iC + 1 Then
'            cOK(i) = iKcbs
'            iKcbs = iKcbs + 1
'        End If
'    Next k
'
'    '�����һ��ѭ����õĳ���С����һ�Σ��򱣴���һ�εĽ��
'    If iKcbs < iMin Then
'        iMin = iKcbs
'        For i = 1 To iC
'            If Left(C(i), 2) = "00" Then CurrentDb.Execute ("update kcYrs set ���α�ʶ=" & cOK(i) & " where �γ̺�='" & C(i) & "'")
'        Next i
'    End If
'Loop
''MsgBox "������" & iLoopCount & "�ι�ѡ��"
''sTime = Timer - sTime
''MsgBox ("ƽ��ÿ�κ�ʱ��" & sTime / iLoopCnt)
'
''��յ��������ͻ'��յ��������ͻ'��յ��������ͻ'��յ��������ͻ'��յ��������ͻ'��յ��������ͻ
''m = DMax("���α�ʶ", "kcYrs") '�ҳ��ǹ�ѡ�����˶��ٳ�
''ReDim ks(m, iiS)
''For i = 1 To m
''    str = "select �γ̺� from kcYrs where ���α�ʶ=" & i
''    Set rs = CurrentDb.OpenRecordset(str)
''    Do While Not rs.EOF
''        n = GetSubscript(C(), Trim(rs("�γ̺�")))
''        For j = 1 To iiS
''            If cs(n, j) = 1 Then ks(i, j) = 1
''        Next j
''        rs.MoveNext
''    Loop
''Next i
''
''For i = 1 To iC
''    If Left(C(i), 2) = "00" Then '�ҳ�Ҫ�ſ��Ĺ�ѡ��
''        iMin = 32767
''        k = 0
''        For j = 1 To m
''            n = ConCount(cs(), i, ks(), j) '�������һ�������ͻ������
''            If iMin > n Then
''                iMin = n
''                k = j
''            End If
''        Next j
''
''        iLoopCount = iLoopCount + iMin '�ۼӳ�ͻ��������
''        CurrentDb.Execute ("update kcYrs set ���α�ʶ=" & k & " where �γ̺�='" & C(i) & "'")
''        For j = 1 To iiS
''            If cs(i, j) = 1 Then ks(k, j) = 1
''        Next j
''    End If
''Next i
''MsgBox "����" & iLoopCount & "�˴γ�ͻ"


Me.�˳�.SetFocus
Me.ȷ��.Enabled = False
DoCmd.Hourglass (False)
End Sub

'�ϲ��γ̵�ͬһ���ο���
Function MergeKc(C() As String, cs() As Byte, a As String, B As String) As Boolean
Dim i As Integer
Dim j As Integer
Dim k As Integer
i = GetSubscript(C(), a)
j = GetSubscript(C(), B)
For k = 1 To UBound(cs, 2)
    If cs(i, k) + cs(j, k) = 2 Then
        MergeKc = False
        Exit Function
    End If
Next k
MergeKc = True
End Function

'�����ж��ٸ�ͬѧ���Գ�ͻ
Function ConCount(cs() As Byte, a As Integer, ks() As Byte, B As Integer) As Integer
Dim i As Integer
Dim j As Integer
For j = 1 To UBound(cs, 2)
    If cs(a, j) + ks(B, j) = 2 Then i = i + 1
Next j
ConCount = i
End Function
Private Sub �˳�_Click()
DoCmd.Close , , acSaveYes
DoCmd.OpenForm "�Ų���", acNormal
End Sub
