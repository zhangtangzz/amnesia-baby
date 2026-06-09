import pytest
from fastapi.testclient import TestClient
from src.api.app import app


class TestKnowledgeAPI:
    """知识库API测试"""

    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)

    def test_process_knowledge(self, client):
        """测试处理知识"""
        request_data = {
            "text": "张三毕业于清华大学，创立了某科技公司",
            "source": "采访视频",
            "character_id": "test_char"
        }
        response = client.post("/api/knowledge/process", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data

    def test_query_knowledge(self, client):
        """测试查询知识"""
        response = client.get("/api/knowledge/query/test_char?keyword=清华")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_knowledge_base(self, client):
        """测试获取知识库"""
        response = client.get("/api/knowledge/base/test_char")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestKnowledgeFileUpload:
    """知识库文件上传测试"""

    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        return TestClient(app)

    def test_upload_txt_file(self, client):
        """测试上传 .txt 文件"""
        import io
        file_content = "张三毕业于清华大学计算机系，后来创立了科技公司。"
        file_data = io.BytesIO(file_content.encode("utf-8"))
        response = client.post(
            "/api/knowledge/upload",
            files={"file": ("test.txt", file_data, "text/plain")},
            data={"source": "test_file", "character_id": "upload_test"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["filename"] == "test.txt"
        assert data["data"]["file_size"] > 0
        assert "profile" in data["data"]
        assert "facts" in data["data"]

    def test_upload_md_file(self, client):
        """测试上传 .md 文件"""
        import io
        file_content = "# 人物简介\n\n李四是一名优秀的工程师。"
        file_data = io.BytesIO(file_content.encode("utf-8"))
        response = client.post(
            "/api/knowledge/upload",
            files={"file": ("bio.md", file_data, "text/markdown")},
            data={"source": "markdown", "character_id": "md_test"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["filename"] == "bio.md"

    def test_upload_unsupported_format(self, client):
        """测试上传不支持的文件格式"""
        import io
        file_data = io.BytesIO(b"some content")
        response = client.post(
            "/api/knowledge/upload",
            files={"file": ("test.pdf", file_data, "application/pdf")},
            data={"source": "test", "character_id": "test"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "格式不支持" in data["message"]

    def test_upload_empty_file(self, client):
        """测试上传空文件"""
        import io
        file_data = io.BytesIO(b"")
        response = client.post(
            "/api/knowledge/upload",
            files={"file": ("empty.txt", file_data, "text/plain")},
            data={"source": "test", "character_id": "test"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "为空" in data["message"]

    def test_upload_oversized_file(self, client):
        """测试上传超大文件"""
        import io
        # 创建超过 5MB 的文件
        file_data = io.BytesIO(b"x" * (6 * 1024 * 1024))
        response = client.post(
            "/api/knowledge/upload",
            files={"file": ("big.txt", file_data, "text/plain")},
            data={"source": "test", "character_id": "test"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "过大" in data["message"]

    def test_upload_csv_file(self, client):
        """测试上传 .csv 文件"""
        import io
        file_content = "姓名,职业,学历\n张三,工程师,博士\n李四,教师,硕士"
        file_data = io.BytesIO(file_content.encode("utf-8"))
        response = client.post(
            "/api/knowledge/upload",
            files={"file": ("data.csv", file_data, "text/csv")},
            data={"source": "csv_data", "character_id": "csv_test"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["filename"] == "data.csv"
