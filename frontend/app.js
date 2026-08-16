const API = "";
let currentPage = "dashboard";
let students = [], professors = [], courses = [];
let modalType = null, modalId = null;

const $ = id => document.getElementById(id);
const esc = s => String(s ?? "").replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));

async function api(path, options={}) {
  const res = await fetch(API + path, {
    ...options,
    headers: {"Content-Type":"application/json", ...(options.headers||{})}
  });
  let data = null;
  try { data = await res.json(); } catch {}
  if (!res.ok) {
    const msg = data?.message || data?.detail || data?.Error || "خطایی در ارتباط با سرور رخ داد.";
    throw new Error(msg);
  }
  return data;
}

function toast(msg, error=false){
  const t=$("toast"); t.textContent=msg; t.className="toast show"+(error?" error":"");
  setTimeout(()=>t.className="toast",2800);
}

async function checkAPI(){
  try{
    await api("/debug/storage");
    $("statusDot").style.background="#10b981";
    $("statusText").textContent="API متصل است";
  }catch(e){
    $("statusDot").style.background="#ef4444";
    $("statusText").textContent="API در دسترس نیست";
  }
}

function goTo(page){
  currentPage=page;
  document.querySelectorAll(".page").forEach(x=>x.classList.remove("active"));
  $(page).classList.add("active");
  document.querySelectorAll(".nav-btn").forEach(x=>x.classList.toggle("active",x.dataset.page===page));
  const titles={dashboard:["داشبورد","نمای کلی سامانه"],students:["دانشجویان","مدیریت دانشجویان"],professors:["اساتید","مدیریت اساتید"],courses:["دروس","مدیریت دروس و اساتید"],selection:["انتخاب واحد","انتخاب و حذف دروس دانشجو"]};
  $("pageTitle").textContent=titles[page][0]; $("pageSubtitle").textContent=titles[page][1];
  refreshCurrentPage();
}
document.querySelectorAll(".nav-btn").forEach(b=>b.onclick=()=>goTo(b.dataset.page));

async function refreshCurrentPage(){
  try{
    if(currentPage==="dashboard") await loadDashboard();
    if(currentPage==="students") await loadStudents();
    if(currentPage==="professors") await loadProfessors();
    if(currentPage==="courses") await loadCourses();
    if(currentPage==="selection"){ await loadStudents(); await loadCourses(); await loadStudentCourses(); }
  }catch(e){toast(e.message,true)}
}

async function loadDashboard(){
  const d=await api("/debug/storage");
  $("studentCount").textContent=d.student_count; $("professorCount").textContent=d.professor_count; $("courseCount").textContent=d.course_count;
}
async function loadStudents(){
  students=await api("/students/");
  $("studentsTable").innerHTML=students.map(s=>`<tr>
    <td>${s.id}</td><td>${esc(s.first_name)} ${esc(s.last_name)}</td><td>${esc(s.student_number)}</td>
    <td>${esc(s.major)}</td><td>${s.selected_courses?.length||0}</td>
    <td class="actions"><button class="btn small secondary" onclick="editStudent(${s.id})">ویرایش</button><button class="btn small danger" onclick="deleteStudent(${s.id})">حذف</button></td>
  </tr>`).join("") || `<tr><td colspan="6">دانشجویی ثبت نشده است.</td></tr>`;
  renderStudentSelect();
}
async function loadProfessors(){
  professors=await api("/professors/");
  $("professorsTable").innerHTML=professors.map(p=>`<tr>
    <td>${p.id}</td><td>${esc(p.first_name)} ${esc(p.last_name)}</td><td>${esc(p.personnel||p.personnel_code)}</td>
    <td>${esc(p.department)}</td><td>${p.courses?.length||0}</td>
    <td class="actions"><button class="btn small secondary" onclick="editProfessor(${p.id})">ویرایش</button><button class="btn small danger" onclick="deleteProfessor(${p.id})">حذف</button></td>
  </tr>`).join("") || `<tr><td colspan="6">استادی ثبت نشده است.</td></tr>`;
}
async function loadCourses(){
  courses=await api("/courses/");
  $("coursesTable").innerHTML=courses.map(c=>{
    const remaining=c["remaining capacity"] ?? Math.max(0,c.capacity-(c.students?.length||0));
    const full=remaining<=0;
    const prof=c.professor ? `${esc(c.professor.first_name)} ${esc(c.professor.last_name)}` : "بدون استاد";
    return `<tr><td>${esc(c.code)}</td><td>${esc(c.title)}</td><td>${c.unit}</td><td>${c.capacity}</td>
      <td><span class="badge ${full?"full":""}">${full ? "تکمیل" : `${remaining} جای خالی`}</span></td>
      <td class="actions"><button class="btn small secondary" onclick="editCourse(${c.id})">ویرایش</button>
      <button class="btn small secondary" onclick="assignProfessor(${c.id})">اختصاص استاد</button>
      <button class="btn small danger" onclick="deleteCourse(${c.id})">حذف</button></td></tr>`;
  }).join("") || `<tr><td colspan="7">درسی ثبت نشده است.</td></tr>`;
  renderCourseCards();
}

function renderStudentSelect(){
  const s=$("selectionStudent"); const old=s.value;
  s.innerHTML=students.map(x=>`<option value="${x.id}">${esc(x.first_name)} ${esc(x.last_name)} — ${esc(x.student_number)}</option>`).join("");
  if(old && students.some(x=>String(x.id)===old)) s.value=old;
}
function renderCourseCards(){
  const selected = new Set((students.find(s=>String(s.id)===$("selectionStudent")?.value)?.selected_courses||[]).map(c=>c.id));
  $("courseCards").innerHTML=courses.map(c=>{
    const remaining=c["remaining capacity"] ?? c.capacity-(c.students?.length||0);
    const picked=selected.has(c.id);
    const prof=c.professor?`${c.professor.first_name} ${c.professor.last_name}`:"بدون استاد";
    return `<div class="course-card"><h4>${esc(c.title)}</h4><p>${esc(c.code)} • ${c.unit} واحد</p><p>استاد: ${esc(prof)}</p><p>ظرفیت: ${c.capacity} | باقی‌مانده: ${remaining}</p>
      <div class="row"><span class="badge ${remaining<=0?"full":""}">${remaining<=0?"تکمیل":"قابل انتخاب"}</span>
      <button class="btn small ${picked?"secondary":"primary"}" ${picked||remaining<=0?"disabled":""} onclick="selectCourse(${c.id})">${picked?"انتخاب شده":"انتخاب درس"}</button></div></div>`;
  }).join("") || "<p>درسی موجود نیست.</p>";
}
async function loadStudentCourses(){
  const sid=$("selectionStudent").value;
  if(!sid){$("selectedCourses").innerHTML="";return}
  try{
    const list=await api(`/students/${sid}/courses`);
    $("selectedCourses").innerHTML=list.map(c=>`<div class="selected-item"><div><b>${esc(c.title)}</b><small> — ${esc(c.code)} • ${c.unit} واحد</small></div><button class="btn small danger" onclick="dropCourse(${c.id})">حذف درس</button></div>`).join("")||"<p>هنوز درسی انتخاب نشده است.</p>";
    renderCourseCards();
  }catch(e){toast(e.message,true)}
}

function openModal(title,html,type,id=null){modalType=type;modalId=id;$("modalTitle").textContent=title;$("modalForm").innerHTML=html;$("modal").classList.remove("hidden")}
function closeModal(){$("modal").classList.add("hidden")}
function input(name,label,value="",required=true){return `<label>${label}<input name="${name}" value="${esc(value)}" ${required?"required":""}></label>`}

function openStudentModal(s=null){
  openModal(s?"ویرایش دانشجو":"ثبت دانشجوی جدید",`<div class="modal-form-grid">${input("first_name","نام",s?.first_name)}${input("last_name","نام خانوادگی",s?.last_name)}${input("student_number","شماره دانشجویی",s?.student_number)}${input("major","رشته",s?.major)}<div class="modal-actions"><button class="btn primary">ذخیره</button><button type="button" class="btn secondary" onclick="closeModal()">انصراف</button></div></div>`,"student",s?.id);
}
function openProfessorModal(p=null){
  openModal(p?"ویرایش استاد":"ثبت استاد جدید",`<div class="modal-form-grid">${input("first_name","نام",p?.first_name)}${input("last_name","نام خانوادگی",p?.last_name)}${input("personnel_code","کد پرسنلی",p?.personnel||p?.personnel_code)}${input("department","گروه آموزشی",p?.department)}<div class="modal-actions"><button class="btn primary">ذخیره</button><button type="button" class="btn secondary" onclick="closeModal()">انصراف</button></div></div>`,"professor",p?.id);
}
function openCourseModal(c=null){
  openModal(c?"ویرایش درس":"ثبت درس جدید",`<div class="modal-form-grid">${input("title","عنوان درس",c?.title)}${input("code","کد درس",c?.code)}<label>ظرفیت<input name="capacity" type="number" min="1" max="200" value="${c?.capacity??30}" required></label><label>تعداد واحد<input name="unit" type="number" min="1" max="5" value="${c?.unit??3}" required></label><div class="modal-actions"><button class="btn primary">ذخیره</button><button type="button" class="btn secondary" onclick="closeModal()">انصراف</button></div></div>`,"course",c?.id);
}

async function submitModal(e){
  e.preventDefault(); const data=Object.fromEntries(new FormData(e.target).entries());
  if(modalType==="course"){data.capacity=Number(data.capacity);data.unit=Number(data.unit)}
  try{
    const base=modalType==="student"?"/students":modalType==="professor"?"/professors":"/courses";
    const method=modalId?"PUT":"POST"; const path=modalId?`${base}/${modalId}`:`${base}/`;
    await api(path,{method,body:JSON.stringify(data)}); closeModal(); toast("عملیات با موفقیت انجام شد"); await refreshCurrentPage();
  }catch(err){toast(err.message,true)}
}

function editStudent(id){openStudentModal(students.find(x=>x.id===id))}
function editProfessor(id){openProfessorModal(professors.find(x=>x.id===id))}
function editCourse(id){openCourseModal(courses.find(x=>x.id===id))}
async function del(path,msg){if(!confirm(msg))return;try{await api(path,{method:"DELETE"});toast("حذف با موفقیت انجام شد");await refreshCurrentPage()}catch(e){toast(e.message,true)}}
function deleteStudent(id){del(`/students/${id}`,"از حذف این دانشجو مطمئن هستید؟")}
function deleteProfessor(id){del(`/professors/${id}`,"از حذف این استاد مطمئن هستید؟")}
function deleteCourse(id){del(`/courses/${id}`,"از حذف این درس مطمئن هستید؟")}

async function assignProfessor(courseId){
  if(!professors.length) await loadProfessors();
  const options=professors.map(p=>`<option value="${p.id}">${esc(p.first_name)} ${esc(p.last_name)} — ${esc(p.personnel||p.personnel_code)}</option>`).join("");
  openModal("اختصاص استاد به درس",`<div class="modal-form-grid"><label>استاد<select name="professor_id" required>${options}</select></label><div class="modal-actions"><button class="btn primary">اختصاص</button><button type="button" class="btn secondary" onclick="closeModal()">انصراف</button></div></div>`,"assign",courseId);
}
async function selectCourse(courseId){
  const sid=$("selectionStudent").value;if(!sid){toast("ابتدا دانشجو را انتخاب کنید.",true);return}
  try{await api(`/students/${sid}/courses/${courseId}`,{method:"POST"});toast("درس با موفقیت انتخاب شد");await loadStudents();await loadCourses();await loadStudentCourses()}catch(e){toast(e.message,true)}
}
async function dropCourse(courseId){
  const sid=$("selectionStudent").value;
  try{await api(`/students/${sid}/courses/${courseId}`,{method:"DELETE"});toast("درس حذف شد");await loadStudents();await loadCourses();await loadStudentCourses()}catch(e){toast(e.message,true)}
}

$("modalForm").addEventListener("submit",async function(e){
  if(modalType!=="assign") return;
});
$("modal").addEventListener("click",e=>{if(e.target.id==="modal")closeModal()});

const originalSubmit=submitModal;
submitModal=async function(e){
  e.preventDefault();
  if(modalType==="assign"){
    const pid=Number(new FormData(e.target).get("professor_id"));
    try{await api(`/courses/${modalId}/professors/${pid}`,{method:"POST"});closeModal();toast("استاد با موفقیت اختصاص داده شد");await loadCourses();await loadProfessors()}catch(err){toast(err.message,true)}
    return;
  }
  return originalSubmit(e);
};

checkAPI(); loadDashboard();
