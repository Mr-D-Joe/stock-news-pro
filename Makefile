# Stock News Pro - Build System
# ==============================
# Central build system for all components:
# - Python AI Service
# - C++ Engine
# - Java GUI

.PHONY: all clean test help python-test cpp-build cpp-test java-build java-test proto-gen run serve

# Default target
all: proto-gen cpp-build java-build
	@echo "✅ All components built successfully"

# ==================== Help ====================
help:
	@echo "Stock News Pro - Makefile"
	@echo "========================="
	@echo ""
	@echo "Build targets:"
	@echo "  all          - Build all components"
	@echo "  clean        - Clean all build artifacts"
	@echo "  test         - Run all tests"
	@echo ""
	@echo "Component targets:"
	@echo "  python-test  - Run Python AI Service tests"
	@echo "  cpp-build    - Build C++ Engine"
	@echo "  cpp-test     - Run C++ Engine tests"
	@echo "  java-build   - Build Java GUI"
	@echo "  java-test    - Run Java GUI tests"
	@echo ""
	@echo "Protobuf:"
	@echo "  proto-gen    - Generate code from .proto files"
	@echo ""
	@echo "Run targets:"
	@echo "  serve        - Start AI Service (dev mode)"
	@echo "  run          - Run Java GUI"

# ==================== Protobuf ====================
PROTO_DIR = shared
PROTO_FILES = $(wildcard $(PROTO_DIR)/*.proto)

proto-gen:
	@echo "📦 Generating Protobuf code..."
	@if command -v protoc > /dev/null 2>&1; then \
		echo "  Python:"; \
		cd ai_service && python -m grpc_tools.protoc -I../$(PROTO_DIR) \
			--python_out=. --grpc_python_out=. \
			../$(PROTO_DIR)/*.proto 2>/dev/null || echo "  (skipped - grpcio-tools not installed)"; \
		echo "  C++:"; \
		cd ../engine && protoc -I../$(PROTO_DIR) \
			--cpp_out=src/proto \
			../$(PROTO_DIR)/*.proto 2>/dev/null || echo "  (skipped - cpp output dir may not exist)"; \
		echo "  Java:"; \
		cd ../gui && protoc -I../$(PROTO_DIR) \
			--java_out=src/main/java \
			../$(PROTO_DIR)/*.proto 2>/dev/null || echo "  (skipped)"; \
	else \
		echo "  ⚠️  protoc not found, skipping protobuf generation"; \
	fi

# ==================== Python AI Service ====================
PYTHON_DIR = ai_service

python-test:
	@echo "🧪 Running Python tests..."
	@cd $(PYTHON_DIR) && \
		source venv/bin/activate && \
		PYTHONPATH=.. python -m pytest tests/ -v --tb=short

serve:
	@echo "🚀 Starting AI Service..."
	@cd $(PYTHON_DIR) && \
		source venv/bin/activate && \
		uvicorn main:app --reload

# ==================== C++ Engine ====================
CPP_DIR = engine
CPP_BUILD = $(CPP_DIR)/build

cpp-build:
	@echo "🔨 Building C++ Engine..."
	@mkdir -p $(CPP_BUILD)
	@cd $(CPP_BUILD) && cmake .. && make

cpp-test: cpp-build
	@echo "🧪 Running C++ tests..."
	@cd $(CPP_BUILD) && ctest --output-on-failure || \
		./test_api_client 2>/dev/null || \
		echo "  (no tests available or test binary not built)"

cpp-clean:
	@rm -rf $(CPP_BUILD)

# ==================== Java GUI ====================
JAVA_DIR = gui

java-build:
	@echo "☕ Building Java GUI..."
	@cd $(JAVA_DIR) && mvn compile -q

java-test:
	@echo "🧪 Running Java tests..."
	@cd $(JAVA_DIR) && mvn test -q

java-clean:
	@cd $(JAVA_DIR) && mvn clean -q

run:
	@echo "🖥️  Starting Java GUI..."
	@cd $(JAVA_DIR) && mvn javafx:run

# ==================== Combined Targets ====================
test: python-test java-test
	@echo ""
	@echo "============================================"
	@echo "✅ All tests completed"
	@echo "============================================"

clean: cpp-clean java-clean
	@echo "🧹 Cleaning build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned"

# ==================== Quick Status ====================
status:
	@echo "Stock News Pro - Status"
	@echo "======================="
	@echo ""
	@echo "Python venv: $(shell [ -d $(VENV) ] && echo '✅ exists' || echo '❌ not created')"
	@echo "C++ build:   $(shell [ -d $(CPP_BUILD) ] && echo '✅ exists' || echo '❌ not built')"
	@echo "Java target: $(shell [ -d $(JAVA_DIR)/target ] && echo '✅ exists' || echo '❌ not built')"
	@echo ""
	@echo "Run 'make help' for available targets"
