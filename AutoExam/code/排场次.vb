Option Compare Database
Option Explicit
Option Base 1

Private Sub 场次复位_Click()
    CurrentDb.Execute ("update kcYrs set 场次标识 = 0")
If testTable("kcYrs预排") Then
    If CurrentData.AllTables("kcYrs预排").IsLoaded Then DoCmd.Close acTable, "kcYrs预排", acSaveNo
    CurrentDb.Execute ("UPDATE kcYrs预排 INNER JOIN kcYrs ON kcYrs预排.课程号 = kcYrs.课程号 SET kcYrs.场次标识 = [kcYrs预排].[场次标识] " _
                    & "WHERE (((kcYrs预排.场次标识)=True))")
End If
Me.kcQuery.Requery
End Sub

Private Sub 考试否复位_Click()
CurrentDb.Execute ("update kcYrs set 不考试 = false where 不考试 = true")
Me.kcQuery.Requery
End Sub

Private Sub 确定_Click()
'**********************************************************************************************************************
'
'特别提示：
'一、班级号用"0000#1"，但若某门课程补考人数大于190人的，就用"0000#2"分流一半，同理若有九百人就用五个班平分；
'二、对于同课程号不同试卷的，一定要用不同的班级号标记，比如用'0000#2'；
'三、双专业的课程班级号用"24002093"；
'四、要分开时间的课程，比如需要放音的听力，提前在【kcYrs】里分好场次；
'五、教室最好用独立的表，因为系统里的教室表太复杂了。
'
'**********************************************************************************************************************
DoCmd.Hourglass (True)
Dim sTime As Single '临时变量，用来测试某程序段的耗时
Dim str As String
Dim l As Long
Dim i As Integer, j As Integer
Dim rs As DAO.Recordset
Dim tKs As Date
tKs = DLookup("ksxq", "Para") '取出考试学期
'sTime = Timer

Dim iLoopCnt As Integer
iLoopCnt = 8

If testTable("xsYxk") Then
    '判断该表是否打开，若打开则强行关闭并删除
    If CurrentData.AllTables("xsYxk").IsLoaded Then DoCmd.Close acTable, "xsYxk", acSaveNo
    CurrentDb.Execute ("drop table xsYxk")
End If

'生成学生与选课子表--------比较费时
str = "SELECT 学生与选课.课程号, 学生与选课.学号, 学生与选课.班级号 INTO xsYxk " _
& "FROM kcYrs INNER JOIN ((学生 INNER JOIN 学生与选课 ON 学生.学号 = 学生与选课.学号) INNER JOIN 班级 ON 学生.班级号 = 班级.班级号) ON kcYrs.课程号 = 学生与选课.课程号 " _
& "WHERE (((学生与选课.开课时间) = #" & tKs & "#) And ((学生与选课.选课状态) = 0 Or (学生与选课.选课状态) Is Null) And ((kcYrs.不考试) = False)) " _
& "ORDER BY 学生与选课.课程号, 学生与选课.学号"
CurrentDb.Execute (str)
CurrentDb.Execute ("alter table xsYxk add column 序号 Byte")
CurrentDb.Execute ("update xsYxk set 序号=1")

Dim iC As Integer '总共要排考的课程门数
Dim iPC As Integer '总共要排考的非公选课门数，即课程程号为非00*的课程
Dim iiS As Integer '总共要排考的学生人数

'计算需排考的学生总数
str = "SELECT DISTINCT 学号 FROM xsYxk"
Set rs = CurrentDb.OpenRecordset(str)
rs.MoveLast
rs.MoveFirst

iiS = rs.RecordCount
iC = DCount("课程号", "kcYrs", "不考试=false")
iPC = DCount("课程号", "kcYrs", "不考试=false ") 'and 课程号 not like '00*'

Dim C() As String '放置需要排考的课程号
ReDim C(iC)

Dim cPre() As Byte '放置预排的场次标识
ReDim cPre(iC)

Dim cOK() As Byte '课程已排的场次标识
ReDim cOK(iC)

Dim S() As String '放置参与选课的学生学号
ReDim S(iiS)

Dim cs() As Byte '放置学生与选课表
ReDim cs(iC, iiS)

i = 1
'对学号数组赋值
Do While Not rs.EOF
    S(i) = Trim(rs("学号"))
    rs.MoveNext
    i = i + 1
Loop

str = "select 课程号 from kcYrs where 不考试=false order by 选课人数 desc"
Set rs = CurrentDb.OpenRecordset(str)
i = 1
'对课程数组赋值
Do While Not rs.EOF
    C(i) = Trim(rs("课程号"))
    rs.MoveNext
    i = i + 1
Loop

Set rs = CurrentDb.OpenRecordset("xsYxk")
Do While Not rs.EOF
'对二维数组赋值--------相当费时--------改了以后好多了
'    For i = 1 To iC
'        If Trim(rs("课程号")) = c(i) Then
'            For j = 1 To iiS
'                If Trim(rs("学号")) = s(j) Then
'                    cs(i, j) = 1
'                End If
'            Next j
'        End If
'    Next i

    i = GetSubscript(C(), Trim(rs("课程号")))
    j = GetSubscript(S(), Trim(rs("学号")))
    cs(i, j) = 1

    rs.MoveNext
Loop

rs.Close
Set rs = Nothing

'========================================================以下开始排考操作========================================================
'先排专业课，后重新在不同的时间段排公选课，不插空档。
Dim iKcbs As Integer
Dim iMin As Integer
Dim k As Integer
Dim m As Integer
Dim n As Integer
Dim iPreMax As Integer '预排的最大场次
iPreMax = DMax("场次标识", "kcYrs")

Dim iPreCount '预排的场次数
iPreCount = DCount("*", "kcYrs", "场次标识>0")

Dim iLoopCount As Integer '临时变量，用来统计给定时间内的排考次数


'先处理预排的课程'''''''''''''''''''''''''''''''''
For i = 1 To iC
    cPre(i) = DLookup("场次标识", "kcYrs", "课程号='" & C(i) & "'")
Next i
'这里加上对预排场次相同的课程进行判断是否有冲突的代码

'先排非公选课========================================================
Randomize
iMin = 32767
'Do While Timer - sTime < 7200
Do While iLoopCount < iLoopCnt
    iLoopCount = iLoopCount + 1

    '对相关数据赋初值，为下一次循环做准备
    iKcbs = 1 + iPreMax
    For k = 1 To iC
        cOK(k) = cPre(k)
    Next k

    For k = 1 To iPC - iPreCount '对整个课程数组的一个大循环
        n = Int(((iPC - iPreCount - k + 1) * Rnd) + 1)
        m = 0
        i = 1

        '找到第n个未排定的课程的下标i
        Do While m < n
            '自2009年上半年开始不对公选课单独处理
            If cOK(i) = 0 Then m = m + 1 'And Left(C(i), 2) <> "00"
            i = i + 1
        Loop
        i = i - 1

        For j = 1 To iC
            If cOK(j) <> 0 Then
                If MergeKc(C(), cs(), C(j), C(i)) = True Then '能和这一时间段的第一门课程合并
                    For l = 1 To iC
                        If l <> j And cOK(l) = cOK(j) Then
                             If MergeKc(C(), cs(), C(l), C(i)) = False Then '但不能和这一时间段的其它课程合并
                                Exit For
                             End If
                        End If
                    Next l

                    If l = iC + 1 Then '能和这一时间段的全部课程合并
                        cOK(i) = cOK(j)
                        Exit For
                    End If
                End If

            End If
        Next j

        '扫描一遍后没能合并，则新开一标识
        If j = iC + 1 Then
            cOK(i) = iKcbs
            iKcbs = iKcbs + 1
        End If
    Next k

    '如果这一次循环求得的场次小于上一次，则保存这一次的结果
    If iKcbs < iMin Then
        iMin = iKcbs
        For i = 1 To iC
            CurrentDb.Execute ("update kcYrs set 场次标识=" & cOK(i) & " where 课程号='" & C(i) & "'")
        Next i
    End If

Loop

''MsgBox "共排了" & iLoopCount & "次非公选课"
'iLoopCount = 0
'
''再排公选课========================================================
''用新时间段'用新时间段'用新时间段'用新时间段'用新时间段'用新时间段'用新时间段'用新时间段
'Dim iLastKcbs As Integer
'iLastKcbs = DMax("场次标识", "kcYrs") '保留非公选课的排考场次数
'iMin = 32767
'Do While iLoopCount < iLoopCnt
'    iLoopCount = iLoopCount + 1
'
'    '对相关数据赋初值，为下一次循环做准备
'    iKcbs = iLastKcbs + 1
'    For k = 1 To iC
'        If Left(C(k), 2) = "00" Then cOK(k) = 0
'    Next k
'
'    For k = 1 To iC - iPC '对整个公选课程数组的一个大循环
'        n = Int(((iC - iPC - k + 1) * Rnd) + 1)
'        m = 0
'        i = 1
'
'        '找到第n个未排定的课程的下标i
'        Do While m < n
'            If cOK(i) = 0 And Left(C(i), 2) = "00" Then m = m + 1
'            i = i + 1
'        Loop
'        i = i - 1
'
'        For j = 1 To iC
'            If cOK(j) <> 0 And Left(C(j), 2) = "00" Then '+++++++++++++++++++++++++++++++++++
'                If MergeKc(C(), cs(), C(j), C(i)) = True Then '能和这一时间段的第一门课程合并
'                    For l = 1 To iC
'                        If l <> j And cOK(l) = cOK(j) Then
'                             If MergeKc(C(), cs(), C(l), C(i)) = False Then '但不能和这一时间段的其它课程合并
'                                Exit For
'                             End If
'                        End If
'                    Next l
'
'                    If l = iC + 1 Then '能和这一时间段的全部课程合并
'                        cOK(i) = cOK(j)
'                        Exit For
'                    End If
'                End If
'
'            End If
'        Next j
'
'        '扫描一遍后没能合并，则新开一标识
'        If j = iC + 1 Then
'            cOK(i) = iKcbs
'            iKcbs = iKcbs + 1
'        End If
'    Next k
'
'    '如果这一次循环求得的场次小于上一次，则保存这一次的结果
'    If iKcbs < iMin Then
'        iMin = iKcbs
'        For i = 1 To iC
'            If Left(C(i), 2) = "00" Then CurrentDb.Execute ("update kcYrs set 场次标识=" & cOK(i) & " where 课程号='" & C(i) & "'")
'        Next i
'    End If
'Loop
''MsgBox "共排了" & iLoopCount & "次公选课"
''sTime = Timer - sTime
''MsgBox ("平均每次耗时：" & sTime / iLoopCnt)
'
''插空档且允许冲突'插空档且允许冲突'插空档且允许冲突'插空档且允许冲突'插空档且允许冲突'插空档且允许冲突
''m = DMax("场次标识", "kcYrs") '找出非公选课排了多少场
''ReDim ks(m, iiS)
''For i = 1 To m
''    str = "select 课程号 from kcYrs where 场次标识=" & i
''    Set rs = CurrentDb.OpenRecordset(str)
''    Do While Not rs.EOF
''        n = GetSubscript(C(), Trim(rs("课程号")))
''        For j = 1 To iiS
''            If cs(n, j) = 1 Then ks(i, j) = 1
''        Next j
''        rs.MoveNext
''    Loop
''Next i
''
''For i = 1 To iC
''    If Left(C(i), 2) = "00" Then '找出要排考的公选课
''        iMin = 32767
''        k = 0
''        For j = 1 To m
''            n = ConCount(cs(), i, ks(), j) '求出与这一场次相冲突的人数
''            If iMin > n Then
''                iMin = n
''                k = j
''            End If
''        Next j
''
''        iLoopCount = iLoopCount + iMin '累加冲突的总人数
''        CurrentDb.Execute ("update kcYrs set 场次标识=" & k & " where 课程号='" & C(i) & "'")
''        For j = 1 To iiS
''            If cs(i, j) = 1 Then ks(k, j) = 1
''        Next j
''    End If
''Next i
''MsgBox "共有" & iLoopCount & "人次冲突"


Me.退出.SetFocus
Me.确定.Enabled = False
DoCmd.Hourglass (False)
End Sub

'合并课程到同一场次考试
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

'计算有多少个同学考试冲突
Function ConCount(cs() As Byte, a As Integer, ks() As Byte, B As Integer) As Integer
Dim i As Integer
Dim j As Integer
For j = 1 To UBound(cs, 2)
    If cs(a, j) + ks(B, j) = 2 Then i = i + 1
Next j
ConCount = i
End Function
Private Sub 退出_Click()
DoCmd.Close , , acSaveYes
DoCmd.OpenForm "排补考", acNormal
End Sub
