# -*- coding: utf-8 -*-
"""题库数据层（第七部分）：排序 / 模拟 / 更多高频题。

补齐偏少的分类，并加入更多经典面试题。
"""

PART7 = [
    {
        "slug": "merge-sorted-array", "lcId": 88, "title": "合并两个有序数组",
        "difficulty": "简单", "tags": ["数组", "双指针", "排序"], "category": "排序",
        "visualizer": "divide-sort.html", "visHint": "归并排序的「合并」步骤",
        "desc": "给你两个按非递减顺序排列的整数数组 nums1 和 nums2，另有两个整数 m 和 n，分别表示 nums1 和 nums2 中的元素数目。请你合并 nums2 到 nums1 中，使合并后的数组同样按非递减顺序排列。注意：最终合并后数组不应由函数返回，而是存储在数组 nums1 中。",
        "examples": [
            {"input": "nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3",
             "output": "[1,2,2,3,5,6]"},
            {"input": "nums1 = [1], m = 1, nums2 = [], n = 0", "output": "[1]"},
        ],
        "hints": ["从后往前填，避免覆盖未处理的元素", "比较两个数组末尾元素，大的放最后"],
        "funcName": "merge_sorted_array",
        "testCases": [
            {"args": [[1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3], "expect": [1, 2, 2, 3, 5, 6]},
            {"args": [[1], 1, [], 0], "expect": [1]},
            {"args": [[0], 0, [1], 1], "expect": [1]},
        ],
        "solutions": [
            {"name": "从后往前双指针", "time": "O(m+n)", "space": "O(1)",
             "idea": "三个指针分别指向 nums1 有效末尾、nums2 末尾、nums1 最终末尾。每次取较大的放到最后，从后往前填，不会覆盖未处理元素。",
             "code": """def merge_sorted_array(nums1, m, nums2, n):
    a = list(nums1[:m])
    b = list(nums2[:n])
    i, j, k = m - 1, n - 1, m + n - 1
    arr = [0] * (m + n)
    while i >= 0 and j >= 0:
        if a[i] > b[j]:
            arr[k] = a[i]; i -= 1
        else:
            arr[k] = b[j]; j -= 1
        k -= 1
    while i >= 0:
        arr[k] = a[i]; i -= 1; k -= 1
    while j >= 0:
        arr[k] = b[j]; j -= 1; k -= 1
    return arr"""},
        ],
    },
    {
        "slug": "relative-sort-array", "lcId": 1122, "title": "数组的相对排序",
        "difficulty": "简单", "tags": ["数组", "排序", "哈希表"], "category": "排序",
        "visualizer": "sort.html", "visHint": "自定义排序规则",
        "desc": "给你两个数组，arr1 和 arr2，arr2 中的元素各不相同，arr2 中的每个元素都出现在 arr1 中。对 arr1 中的元素进行排序，使 arr1 中项的相对顺序和 arr2 中的相对顺序相同。未在 arr2 中出现过的元素需要按照升序放在 arr1 的末尾。",
        "examples": [
            {"input": "arr1 = [2,3,1,3,2,4,6,7,9,2,19], arr2 = [2,1,4,3,9,6]",
             "output": "[2,2,2,1,4,3,3,9,6,7,19]"},
        ],
        "hints": ["用计数排序的思想", "先按 arr2 的顺序输出，再把剩余的升序输出"],
        "funcName": "relative_sort_array",
        "testCases": [
            {"args": [[2,3,1,3,2,4,6,7,9,2,19], [2,1,4,3,9,6]],
             "expect": [2,2,2,1,4,3,3,9,6,7,19]},
            {"args": [[28,6,22,8,44,17], [22,28,8,6]],
             "expect": [22,28,8,6,17,44]},
        ],
        "solutions": [
            {"name": "计数 + 按序输出", "time": "O(n + max)", "space": "O(max)",
             "idea": "统计 arr1 中每个数出现次数。先按 arr2 的顺序输出对应数量的元素，再把没出现在 arr2 中的数按升序输出。",
             "code": """def relative_sort_array(arr1, arr2):
    from collections import Counter
    cnt = Counter(arr1)
    res = []
    for x in arr2:
        res.extend([x] * cnt.pop(x, 0))
    for x in sorted(cnt):
        res.extend([x] * cnt[x])
    return res"""},
        ],
    },
    {
        "slug": "top-k-frequent", "lcId": 347, "title": "前 K 个高频元素",
        "difficulty": "中等", "tags": ["数组", "哈希表", "堆", "排序"], "category": "排序",
        "visualizer": "heap.html", "visHint": "堆的 Top-K 应用（按频次排序）",
        "desc": "给你一个整数数组 nums 和一个整数 k，请你返回其中出现频率前 k 高的元素。你可以按任意顺序返回答案。",
        "examples": [
            {"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]"},
            {"input": "nums = [1], k = 1", "output": "[1]"},
        ],
        "hints": ["先统计频率", "用大小为 k 的小根堆维护前 k 高频"],
        "funcName": "top_k_frequent",
        "testCases": [
            {"args": [[1, 1, 1, 2, 2, 3], 2], "expect": [1, 2]},
            {"args": [[1], 1], "expect": [1]},
            {"args": [[1, 2], 2], "expect": [1, 2]},
        ],
        "solutions": [
            {"name": "哈希计数 + 按频次排序", "time": "O(n log n)", "space": "O(n)",
             "idea": "用 Counter 统计频率，然后按频率降序排序，取前 k 个。写法最简单。",
             "code": """def top_k_frequent(nums, k):
    from collections import Counter
    cnt = Counter(nums)
    ordered = sorted(cnt.items(), key=lambda kv: -kv[1])
    return [x for x, _ in ordered[:k]]"""},
            {"name": "小根堆（O(n log k)）", "time": "O(n log k)", "space": "O(n)",
             "idea": "用大小为 k 的小根堆（按频次比较）筛选，堆里始终保留频次最高的 k 个。",
             "code": """import heapq
from collections import Counter

def top_k_frequent(nums, k):
    cnt = Counter(nums)
    heap = []
    for x, c in cnt.items():
        heapq.heappush(heap, (c, x))
        if len(heap) > k:
            heapq.heappop(heap)
    return [x for _, x in heap]"""},
        ],
    },
    {
        "slug": "spiral-matrix", "lcId": 54, "title": "螺旋矩阵",
        "difficulty": "中等", "tags": ["数组", "矩阵", "模拟"], "category": "模拟与进阶",
        "visualizer": None, "visHint": None,
        "desc": "给你一个 m 行 n 列的矩阵 matrix，请按照顺时针螺旋顺序，返回矩阵中的所有元素。",
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[1,2,3,6,9,8,7,4,5]"},
            {"input": "matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]",
             "output": "[1,2,3,4,8,12,11,10,9,5,6,7]"},
        ],
        "hints": ["维护上下左右四个边界", "每走完一条边就收缩对应边界"],
        "funcName": "spiral_order",
        "testCases": [
            {"args": [[[1,2,3],[4,5,6],[7,8,9]]], "expect": [1,2,3,6,9,8,7,4,5]},
            {"args": [[[1,2,3,4],[5,6,7,8],[9,10,11,12]]], "expect": [1,2,3,4,8,12,11,10,9,5,6,7]},
            {"args": [[[1]]], "expect": [1]},
        ],
        "solutions": [
            {"name": "边界收缩法", "time": "O(m×n)", "space": "O(1)",
             "idea": "维护 top/bottom/left/right 四个边界。依次从左到右、从上到下、从右到左、从下到上遍历，每完成一条边就收缩对应边界，直到边界交叉。",
             "code": """def spiral_order(matrix):
    if not matrix:
        return []
    res = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            res.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            res.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                res.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                res.append(matrix[r][left])
            left += 1
    return res"""},
        ],
    },
    {
        "slug": "set-matrix-zeroes", "lcId": 73, "title": "矩阵置零",
        "difficulty": "中等", "tags": ["数组", "矩阵", "模拟"], "category": "模拟与进阶",
        "visualizer": None, "visHint": None,
        "desc": "给定一个 m x n 的矩阵，如果一个元素为 0，则将其所在行和列的所有元素都设为 0。请使用原地算法。",
        "examples": [
            {"input": "matrix = [[1,1,1],[1,0,1],[1,1,1]]",
             "output": "[[1,0,1],[0,0,0],[1,0,1]]"},
        ],
        "hints": ["不要边遍历边改（会影响后续判断）", "先记录哪些行列需要置零，再统一处理"],
        "funcName": "set_zeroes",
        "testCases": [
            {"args": [[[1,1,1],[1,0,1],[1,1,1]]], "expect": [[1,0,1],[0,0,0],[1,0,1]]},
            {"args": [[[0,1,2,0],[3,4,5,2],[1,3,1,5]]],
             "expect": [[0,0,0,0],[0,4,5,0],[0,3,1,0]]},
        ],
        "solutions": [
            {"name": "先标记后置零", "time": "O(m×n)", "space": "O(m+n)",
             "idea": "先扫描一遍记录哪些行、哪些列包含 0，然后再扫描一遍把对应行列置零。这样避免「边改边判断」导致的错误传播。",
             "code": """def set_zeroes(matrix):
    rows, cols = len(matrix), len(matrix[0])
    zero_rows, zero_cols = set(), set()
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 0:
                zero_rows.add(r)
                zero_cols.add(c)
    for r in range(rows):
        for c in range(cols):
            if r in zero_rows or c in zero_cols:
                matrix[r][c] = 0
    return matrix"""},
        ],
    },
    {
        "slug": "fizz-buzz", "lcId": 412, "title": "Fizz Buzz",
        "difficulty": "简单", "tags": ["数学", "字符串", "模拟"], "category": "模拟与进阶",
        "visualizer": None, "visHint": None,
        "desc": "给你一个整数 n，找出从 1 到 n 各个整数的 Fizz Buzz 表示，并用字符串数组 answer（下标从 1 开始）返回结果，其中：answer[i] == \"FizzBuzz\" 如果 i 同时是 3 和 5 的倍数；answer[i] == \"Fizz\" 如果 i 是 3 的倍数；answer[i] == \"Buzz\" 如果 i 是 5 的倍数；answer[i] == i 如果上述条件全不满足。",
        "examples": [
            {"input": "n = 3", "output": '["1","2","Fizz"]'},
            {"input": "n = 5", "output": '["1","2","Fizz","4","Buzz"]'},
        ],
        "hints": ["先判断同时是 3 和 5 的倍数", "注意判断顺序"],
        "funcName": "fizz_buzz",
        "testCases": [
            {"args": [3], "expect": ["1", "2", "Fizz"]},
            {"args": [5], "expect": ["1", "2", "Fizz", "4", "Buzz"]},
            {"args": [15], "expect": ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz",
                                      "11","Fizz","13","14","FizzBuzz"]},
        ],
        "solutions": [
            {"name": "逐个数判断", "time": "O(n)", "space": "O(1)",
             "idea": "从 1 到 n 遍历，依次判断是否为 15、3、5 的倍数，注意 15 的判断必须放最前面。",
             "code": """def fizz_buzz(n):
    res = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            res.append("FizzBuzz")
        elif i % 3 == 0:
            res.append("Fizz")
        elif i % 5 == 0:
            res.append("Buzz")
        else:
            res.append(str(i))
    return res"""},
        ],
    },
    {
        "slug": "single-number", "lcId": 136, "title": "只出现一次的数字",
        "difficulty": "简单", "tags": ["位运算", "数组"], "category": "数组与哈希",
        "visualizer": None, "visHint": None,
        "desc": "给你一个非空整数数组 nums，除了某个元素只出现一次以外，其余每个元素均出现两次。找出那个只出现了一次的元素。你必须设计并实现线性时间复杂度的算法来解决此问题，且该算法只使用常量额外空间。",
        "examples": [
            {"input": "nums = [2,2,1]", "output": "1"},
            {"input": "nums = [4,1,2,1,2]", "output": "4"},
        ],
        "hints": ["异或运算：a ^ a = 0，a ^ 0 = a", "把所有数异或起来，成对的会抵消"],
        "funcName": "single_number",
        "testCases": [
            {"args": [[2, 2, 1]], "expect": 1},
            {"args": [[4, 1, 2, 1, 2]], "expect": 4},
            {"args": [[1]], "expect": 1},
        ],
        "solutions": [
            {"name": "异或（最优）", "time": "O(n)", "space": "O(1)",
             "idea": "利用异或的性质：相同的数异或为 0，任何数与 0 异或等于它本身。把所有数异或起来，成对出现的都抵消了，剩下的就是只出现一次的数。",
             "code": """def single_number(nums):
    result = 0
    for x in nums:
        result ^= x
    return result"""},
            {"name": "哈希集合", "time": "O(n)", "space": "O(n)",
             "idea": "用一个集合：元素不在集合里就加入，已在集合里就移除。最后剩下的就是答案。思路更直观，但需要额外空间。",
             "code": """def single_number(nums):
    seen = set()
    for x in nums:
        if x in seen:
            seen.remove(x)
        else:
            seen.add(x)
    return seen.pop()"""},
        ],
    },
    {
        "slug": "missing-number", "lcId": 268, "title": "丢失的数字",
        "difficulty": "简单", "tags": ["位运算", "数组", "数学"], "category": "数组与哈希",
        "visualizer": None, "visHint": None,
        "desc": "给定一个包含 [0, n] 中 n 个数的数组 nums，找出 [0, n] 这个范围内没有出现在数组中的那个数。",
        "examples": [
            {"input": "nums = [3,0,1]", "output": "2"},
            {"input": "nums = [0,1]", "output": "2"},
            {"input": "nums = [9,6,4,2,3,5,7,0,1]", "output": "8"},
        ],
        "hints": ["用等差数列求和公式算出总和，减去实际和", "或用异或"],
        "funcName": "missing_number",
        "testCases": [
            {"args": [[3, 0, 1]], "expect": 2},
            {"args": [[0, 1]], "expect": 2},
            {"args": [[9, 6, 4, 2, 3, 5, 7, 0, 1]], "expect": 8},
        ],
        "solutions": [
            {"name": "数学求和", "time": "O(n)", "space": "O(1)",
             "idea": "0 到 n 的和是 n(n+1)/2。用这个理论总和减去数组实际总和，差值就是缺失的数。",
             "code": """def missing_number(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)"""},
            {"name": "异或", "time": "O(n)", "space": "O(1)",
             "idea": "把 0..n 和数组所有元素一起异或，成对出现的抵消，剩下就是缺失的数。可以避免大数求和溢出（在 Python 中不必要，但思路通用）。",
             "code": """def missing_number(nums):
    result = len(nums)
    for i, x in enumerate(nums):
        result ^= i ^ x
    return result"""},
        ],
    },
    {
        "slug": "majority-element", "lcId": 169, "title": "多数元素",
        "difficulty": "简单", "tags": ["数组", "哈希表", "分治", "贪心"], "category": "贪心",
        "visualizer": None, "visHint": None,
        "desc": "给定一个大小为 n 的数组 nums，返回其中的多数元素。多数元素是指在数组中出现次数大于 ⌊n/2⌋ 的元素。你可以假设数组是非空的，并且给定的数组总是存在多数元素。",
        "examples": [
            {"input": "nums = [3,2,3]", "output": "3"},
            {"input": "nums = [2,2,1,1,1,2,2]", "output": "2"},
        ],
        "hints": ["Boyer-Moore 投票算法：不同就抵消", "因为多数元素出现次数过半，剩下的必然是它"],
        "funcName": "majority_element",
        "testCases": [
            {"args": [[3, 2, 3]], "expect": 3},
            {"args": [[2, 2, 1, 1, 1, 2, 2]], "expect": 2},
            {"args": [[1]], "expect": 1},
        ],
        "solutions": [
            {"name": "Boyer-Moore 投票算法", "time": "O(n)", "space": "O(1)",
             "idea": "维护一个候选元素和计数器。遇到相同元素计数 +1，不同则 -1；计数归零就换候选。因为多数元素出现次数过半，最后剩下的候选必然是它。",
             "code": """def majority_element(nums):
    candidate = None
    count = 0
    for x in nums:
        if count == 0:
            candidate = x
        count += 1 if x == candidate else -1
    return candidate"""},
        ],
    },
]
