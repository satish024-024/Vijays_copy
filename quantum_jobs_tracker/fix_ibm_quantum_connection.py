#!/usr/bin/env python3
"""
Fix IBM Quantum connection to use proper qiskit-ibm-runtime implementation
"""

def fix_ibm_quantum_connection():
    """Fix the IBM Quantum connection to use proper CRN-based connection"""
    
    file_path = 'real_quantum_app.py'
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Remove the automatic connection during initialization
    old_init = '''        # Only try to connect if we have a token
        if self.token and self.token.strip():
            print("   🔌 STARTING REAL IBM QUANTUM CONNECTION PROCESS...")
            print("   📡 Connecting to IBM Quantum (non-blocking)...")
            print("   ⏳ Connection will happen in background...")
            # Initialize connection in background to avoid hanging
            self._initialize_quantum_connection_async()
        else:
            print("   ⚠️  NO TOKEN PROVIDED - using sample data mode")
            print("   💡 To see real IBM Quantum data, set IBM_QUANTUM_TOKEN environment variable")
            print("🔄 Quantum manager initialized with sample data mode")
            self.is_connected = False'''

    new_init = '''        # Don't connect during initialization - wait until first API call
        if self.token and self.token.strip():
            print("   🔌 IBM QUANTUM TOKEN PROVIDED - connection will happen on first API call")
            print("   📡 Real IBM Quantum data will be available after authentication")
        else:
            print("   ⚠️  NO TOKEN PROVIDED - using sample data mode")
            print("   💡 To see real IBM Quantum data, set IBM_QUANTUM_TOKEN environment variable")
        
        print("🔄 Quantum manager initialized (lazy connection)")
        self.is_connected = False'''
    
    if old_init in content:
        content = content.replace(old_init, new_init)
        print("✅ Fixed automatic connection during initialization")
    else:
        print("⚠️ Could not find the exact initialization code to replace")
        return False
    
    # Fix 2: Replace the complex connection logic with proper IBM Cloud Quantum Computing service connection
    old_connection_logic = '''            # Try different instance configurations in order of preference
            instances_to_try = []

            # Add user CRN if provided
            if self.crn and self.crn.strip():
                instances_to_try.append(self.crn)

            # Add common public instances for fallback
            instances_to_try.extend([
                "ibm-q/open/main",  # Main public instance
                "ibm-q/open/ibm-q-yorktown/main",
                "ibm-q/open/ibm-q-armonk/main",
                None  # Try without instance as last resort
            ])

            connection_successful = False

            for instance in instances_to_try:
                try:
                    if instance:
                        print(f"🔄 Trying instance: {instance}")
                        service = qiskit_ibm_runtime.QiskitRuntimeService(
                            channel="ibm_cloud",
                            token=self.token,
                            instance=instance
                        )
                    else:
                        print("🔄 Trying without instance (public access)")
                        service = qiskit_ibm_runtime.QiskitRuntimeService(
                            channel="ibm_quantum",
                            token=self.token
                        )'''

    new_connection_logic = '''            # Connect to IBM Cloud Quantum Computing service using CRN
            connection_successful = False
            
            try:
                if self.crn and self.crn.strip():
                    print(f"🔄 Connecting to IBM Cloud Quantum Computing service with CRN...")
                    service = qiskit_ibm_runtime.QiskitRuntimeService(
                        channel="ibm_cloud",
                        token=self.token,
                        instance=self.crn
                    )
                else:
                    print("🔄 Trying public IBM Quantum access...")
                    service = qiskit_ibm_runtime.QiskitRuntimeService(
                        channel="ibm_quantum",
                        token=self.token
                    )'''
    
    if old_connection_logic in content:
        content = content.replace(old_connection_logic, new_connection_logic)
        print("✅ Fixed connection logic to use proper CRN-based connection")
    else:
        print("⚠️ Could not find the exact connection logic to replace")
        return False
    
    # Fix 3: Simplify the connection test logic
    old_test_logic = '''                    # Test the connection by trying to list backends with timeout
                    print("🔍 Testing connection by fetching backends...")
                    
                    # Use threading-based timeout for Windows compatibility
                    import threading
                    import queue
                    
                    def fetch_backends_with_timeout(service, result_queue, timeout=30):
                        try:
                            backends = service.backends()
                            result_queue.put(('success', backends))
                        except Exception as e:
                            result_queue.put(('error', e))
                    
                    result_queue = queue.Queue()
                    thread = threading.Thread(target=fetch_backends_with_timeout, args=(service, result_queue, 30))
                    thread.daemon = True
                    thread.start()
                    thread.join(timeout=30)
                    
                    if thread.is_alive():
                        print(f"⏰ Connection timeout for instance: {instance}")
                        continue
                    
                    if result_queue.empty():
                        print(f"⏰ Connection timeout for instance: {instance}")
                        continue
                    
                    result_type, result_data = result_queue.get()
                    
                    if result_type == 'success':
                        print(f"✅ Successfully connected to IBM Quantum instance: {instance}")
                        print(f"📊 Found {len(result_data)} backends")
                        self.provider = service
                        self.is_connected = True
                        connection_successful = True
                        break
                    else:
                        print(f"❌ Instance {instance} failed: {result_data}")
                        continue
                        
                except Exception as instance_error:
                    print(f"❌ Instance {instance} failed: {instance_error}")
                    continue'''

    new_test_logic = '''                # Test the connection by trying to list backends with timeout
                print("🔍 Testing connection by fetching backends...")
                
                # Use threading-based timeout for Windows compatibility
                import threading
                import queue
                
                def fetch_backends_with_timeout(service, result_queue, timeout=30):
                    try:
                        backends = service.backends()
                        result_queue.put(('success', backends))
                    except Exception as e:
                        result_queue.put(('error', e))
                
                result_queue = queue.Queue()
                thread = threading.Thread(target=fetch_backends_with_timeout, args=(service, result_queue, 30))
                thread.daemon = True
                thread.start()
                thread.join(timeout=30)
                
                if thread.is_alive():
                    print(f"⏰ Connection timeout")
                    raise Exception("Connection timeout")
                
                if result_queue.empty():
                    print(f"⏰ Connection timeout")
                    raise Exception("Connection timeout")
                
                result_type, result_data = result_queue.get()
                
                if result_type == 'success':
                    print(f"✅ Successfully connected to IBM Quantum service")
                    print(f"📊 Found {len(result_data)} backends")
                    self.provider = service
                    self.is_connected = True
                    connection_successful = True
                else:
                    print(f"❌ Connection failed: {result_data}")
                    raise Exception(f"Connection failed: {result_data}")
                    
            except Exception as connection_error:
                print(f"❌ Connection failed: {connection_error}")'''
    
    if old_test_logic in content:
        content = content.replace(old_test_logic, new_test_logic)
        print("✅ Fixed connection test logic")
    else:
        print("⚠️ Could not find the exact test logic to replace")
        return False
    
    # Fix 4: Add lazy connection method
    lazy_connection_method = '''
    def _ensure_connection(self):
        """Ensure connection is established before making API calls"""
        if not self.is_connected and self.token and self.token.strip():
            print("🔌 Establishing IBM Quantum connection on demand...")
            try:
                self._initialize_quantum_connection()
                print("✅ Connection established successfully")
            except Exception as e:
                print(f"❌ Connection failed: {e}")
                self.is_connected = False'''
    
    # Find where to insert the lazy connection method
    insert_point = "def connect_with_credentials(self, token, crn=None):"
    if insert_point in content:
        content = content.replace(insert_point, lazy_connection_method + "\n    " + insert_point)
        print("✅ Added lazy connection method")
    else:
        print("⚠️ Could not find insertion point for lazy connection method")
        return False
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Successfully fixed IBM Quantum connection")
    print("✅ Connection now uses proper CRN-based IBM Cloud Quantum Computing service")
    print("✅ Lazy connection prevents infinite loops during initialization")
    return True

if __name__ == "__main__":
    fix_ibm_quantum_connection()
